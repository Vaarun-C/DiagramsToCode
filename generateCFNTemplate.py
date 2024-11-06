import os
from ultralytics import YOLO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict, deque
import copy
import networkx as nx
import matplotlib.pyplot as plt

URI = "mongodb+srv://CapTheStone:VarunVikas@viewme.vzrbu.mongodb.net/?retryWrites=true&w=majority&appName=viewme"
icons_collection = None
model_names = None

class Node:
    ID = 0  # Static variable to assign unique IDs to each node

    def __init__(self, type_name:str, unit_template:dict):
        self.id = Node.ID
        Node.ID += 1
        self.type_name = type_name
        self.unit_template = unit_template
        self.dependencies = unit_template.get("Dependencies", []) # dependency types
        self.dependency_edges = []  # Stores IDs of dependent nodes
        self.replaceMap = {}
        self.consumedBy = set() # set of all types that have their dependency assigned to this node

    def setData(self, data):
        node_name = self.replaceMap[self.type_name]
        for key in self.unit_template:
            if key in ('Type', '_id', 'Dependencies'):
                continue
            value:str = self.unit_template[key]
            value = value.replace('$$1', node_name)
            for i, dep_type in enumerate(self.dependencies):
                dep_name = self.replaceMap[dep_type]
                value = value.replace(f'$${i + 2}', dep_name)

            data[key] += f'\n{value}'

    def __repr__(self):
        return f"Node({self.type_name}, id={self.id})"

class Graph:
    def __init__(self):
        self.nodes:dict[int,Node] = {} # ID -> Node
        self.stored_types:dict[str,list[int]] = {} # type -> list[ID]
        self.in_degree = defaultdict(int)
        self.type_dict = {}
        self.DG = nx.DiGraph()

    def add_node(self, node:Node):
        self.nodes[node.id] = node
        # if node.type_name in SHAREABLE_RESOURCES:
        self.stored_types.setdefault(node.type_name, []).append(node.id)
        self.DG.add_node(f"{node.type_name.replace("AWS::", "")}-{node.id}")

    def add_edge(self, from_node:Node, to_node:Node):
        """adds the edge in the reverse direction"""
        to_node.dependency_edges.append(from_node.id)
        self.in_degree[from_node.id] += 1
        self.DG.add_edge(f"{from_node.type_name.replace("AWS::", "")}-{from_node.id}", f"{to_node.type_name.replace("AWS::", "")}-{to_node.id}")

    def edge_exists(self, from_node:Node, to_node:Node):
        """Checks if an edge exists"""
        return from_node.id in to_node.dependency_edges

    def topological_sort_out_degree(self):
        zero_in_degree_queue = deque([node for node in self.nodes.values() if self.in_degree[node.id] == 0])
        sorted_order = []
        while zero_in_degree_queue:
            node = zero_in_degree_queue.popleft()
            sorted_order.append(node)

            # For each outgoing edge from the node, reduce the in-degree of the target node
            for dep_id in node.dependency_edges:
                # Find the dependent node by ID
                dep_node = self.nodes[dep_id]
                self.in_degree[dep_id] -= 1
                if self.in_degree[dep_id] == 0:
                    zero_in_degree_queue.append(dep_node)

        # If sorted_order contains all nodes, return it; otherwise, there's a cycle
        if len(sorted_order) == len(self.nodes):
            return sorted_order
        else:
            raise ArithmeticError("Cycle Detected! Topological Sort Not possible")
        
    def print_graph(self, file_name):
        # nx.draw(self.DG, with_labels=True, font_weight='bold')
        # nx.draw_circular(self.DG, with_labels=True, font_weight='bold')
        nx.draw_shell(self.DG, with_labels=True, font_weight='bold', node_size=max(5, 100/len(list(self.DG.nodes))), font_size=max(1, 100/len(list(self.DG.nodes))), edge_color="grey")
        # nx.draw_shell(self.DG, with_labels=True, font_weight='bold')
        # nx.draw_planar(self.DG, with_labels=True, font_weight='bold')
        # nx.draw_spectral(self.DG, with_labels=True, font_weight='bold')
        # nx.draw_spring(self.DG, with_labels=True, font_weight='bold')
        plt.savefig(file_name, dpi=600)
        plt.clf()

CLS_NAME_TO_TYPE = {
    "Arch_Amazon-Elastic-Container-Service_64": "AWS::ECS::Cluster",
    "Arch_Amazon-Simple-Storage-Service_64": "AWS::S3::Bucket",
    "Arch_AWS-Lambda_64": "AWS::Lambda::Function",
    "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance",
    "Arch_AWS-Fargate_64": "AWS::ECS::Cluster"
}

LLM_SUGGESTIONS = {
    'AWS::ECS::Cluster': [
        'AWS::ECS::TaskDefinition',
        'AWS::ECS::Service'
    ],

    'AWS::EC2::VPC': [
        'AWS::EC2::InternetGateway',
        'AWS::EC2::RouteTable',
        'AWS::EC2::Route',
        'AWS::EC2::VPCGatewayAttachment',
        'AWS::EC2::SubnetRouteTableAssociation'
    ],

    'AWS::S3::Bucket': [
        'AWS::S3::BucketPolicy'
    ],

    'AWS::Lambda::Function': [
        'AWS::ApiGateway::RestApi',
        'AWS::ApiGateway::Resource',
        'AWS::ApiGateway::MethodForLambda',
        'AWS::Lambda::Permission'
    ],
}

SHAREABLE_RESOURCES = {
    'AWS::EC2::VPC',
    'AWS::EC2::Subnet',
    'AWS::EC2::InternetGateway',
    'AWS::EC2::VPCGatewayAttachment',
    'AWS::EC2::RouteTable',
    'AWS::EC2::Route',
    'AWS::IAM::RoleForLambda',
    'AWS::DynamoDB::Table',
    'AWS::ECS::Cluster',
    'AWS::ApiGateway::RestApi'
}

def connect_to_mongo():
    client = MongoClient(URI, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        print("CONNECTION ERROR!!")
        quit()

def get_detected_types(result) -> list[str]:
    detected_classes_types = []
    for box in result.boxes: # type: ignore
        class_id = int(box.cls) # Get the class id for the current box
        class_name = model_names[class_id]# Get the class name from the model's names list
        try:
            detected_classes_types.append(CLS_NAME_TO_TYPE[class_name])
        except:
            print(class_name, "not in Mongo yet !!!!")
    return detected_classes_types

def get_LLM_types(class_types:list[str]):
    new_types = []
    for class_type in class_types:
        new_types.extend(LLM_SUGGESTIONS.get(class_type, []))
    return new_types

def fetch_document_from_mongo(type_name):
    document = icons_collection.find_one({"Type": type_name})
    if not document:
        raise LookupError(f'[{type_name}] does not exist in Database')
    return document

def createNode(type_name) -> Node:
    unit_template = fetch_document_from_mongo(type_name)
    node:Node = Node(type_name, unit_template)
    return node

def get_or_makeNode(type_name, dep_type_name, graph:Graph, queue:deque) -> Node:
    if (len(graph.stored_types.get(dep_type_name, [])) == 0):
        dep_node:Node = createNode(dep_type_name)
        graph.add_node(dep_node)
        queue.append(dep_node)
    else:
        # Always chooses first existing node. Need to change with either groups info or something else
        candidate_dep_node_ids = graph.stored_types[dep_type_name]
        if dep_type_name in SHAREABLE_RESOURCES:
            dep_node_id = candidate_dep_node_ids[0] 
        else: 
            # dep_type_name in Unique
            for candidate_node_id in candidate_dep_node_ids:
                candidate_node = graph.nodes[candidate_node_id]
                if type_name not in candidate_node.consumedBy:
                    candidate_node.consumedBy.add(type_name)
                    dep_node_id = candidate_node_id
                    break
        dep_node:Node = graph.nodes[dep_node_id]
    return dep_node

def build_graph_from_types(class_types:list[str]):
    node_queue = deque()
    graph = Graph()

    suggested_types = get_LLM_types(class_types=class_types)
    class_types.extend(suggested_types)

    for class_type in class_types:
        try:
            node:Node = createNode(class_type)
            graph.add_node(node)
            node_queue.append(node)
        except LookupError as e:
            print(f"No additional details found for class {class_type}", e)
    
    while node_queue:
        node:Node = node_queue.popleft()
        print(f"Creating Node for: {node}")
        # Add dependency nodes
        for dependency_type in node.dependencies:
            dep_node = get_or_makeNode(node.type_name, dependency_type, graph=graph, queue=node_queue)
            print(f"Adding Edge for dependency: {dep_node}")
            graph.add_edge(node, dep_node)

    ids_to_remove = []
    for id, node in graph.nodes.items():
        if (node.type_name in SHAREABLE_RESOURCES) and (len(node.dependency_edges) == 0):
            ids_to_remove.append(id)

            # remove from networkX
            graph.DG.remove_node(f"{node.type_name.replace("AWS::", "")}-{id}")

    new_nodes = {}
    for id, node in graph.nodes.items():
        if (id in ids_to_remove):
            continue
        new_nodes[id] = graph.nodes[id]


    graph.nodes = new_nodes
    
    return graph

def createName(type_name:str, graph:Graph):
    graph.type_dict[type_name] = graph.type_dict.get(type_name,0) + 1
    name = 'My'+type_name.split("::")[-1] + str(graph.type_dict[type_name])
    return name

def create_template(result, file_name):
    data = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": f"CloudFormation Template for {file_name}",
        "Conditions": "",
        "Parameters": "",
        "Resources": "",
        "Outputs": ""
    }

    # Get detected classes
    detected_classes_types:list[str] = get_detected_types(result)
    graph = build_graph_from_types(detected_classes_types)
    sorted_nodes:list[Node] = graph.topological_sort_out_degree()

    for node in sorted_nodes:
        node_name = createName(node.type_name, graph=graph)
        node.replaceMap[node.type_name] = node_name
        for nbr_id in node.dependency_edges:
            graph.nodes[nbr_id].replaceMap[node.type_name] = node_name
        node.setData(data)

    graph.print_graph(file_name)
    # input()

    return data

def runModelOn(path,*, weights):
    global model_names

    all_classes = set(range(298))
    removed_classes = set([57]) #
    allowed_classes = list(all_classes-removed_classes)

    # Predict using best weights from the model
    model = YOLO(weights)
    results = model.predict(path, save=True, line_width=1, classes=allowed_classes, conf=0.6)
    model_names = model.names
    return results
    
def main():
    global icons_collection
    output_path = 'testCFNTemplates'
    weight_for_model = "298_icons_best.pt"
    architecture_path = "./test/distributed-load-testing-on-aws-architecture.dc386721ef6865bf5ed7c3e68a9af324a3bb2d83.png"
    assert weight_for_model in os.listdir(), "Model Weights missing!"

    # Make directories if they don't exist
    os.makedirs(output_path, exist_ok=True)

    client = connect_to_mongo()
    db = client['Templates']
    icons_collection = db['Templates[PROD]_cleaned']

    results = runModelOn(architecture_path, weights=weight_for_model)
    for i, result in enumerate(results):
        data = create_template(result, result.path.split('/')[-1])

        with open(output_path + f"/template{i}.yaml", 'w') as file:
            for k, v in data.items():
                file.write(f"{k}: {v.replace('\\n', '\n')}\n")

if '__main__' == __name__:
    main()