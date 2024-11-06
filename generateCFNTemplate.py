import os
import yaml
from ultralytics import YOLO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict, deque
import json
import colorama

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

            data[key] += f'\n  {value}'

    def __repr__(self):
        return f"Node({self.type_name}, id={self.id})"


class Graph:
    def __init__(self):
        self.nodes:dict[int,Node] = {} # ID -> Node
        self.stored_types:dict[str,list[int]] = {} # type -> list[ID]
        self.in_degree = defaultdict(int)

    def add_node(self, node:Node):
        self.nodes[node.id] = node
        self.stored_types.setdefault(node.type_name, []).append(node.id)

    def add_edge(self, from_node:Node, to_node:Node):
        """adds the edge in the reverse direction"""
        to_node.dependency_edges.append(from_node.id)
        self.in_degree[from_node.id] += 1

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


CLS_NAME_TO_TYPE = {
    "Arch_Amazon-Elastic-Container-Service_64": "AWS::ECS::Cluster",
    "Arch_Amazon-Simple-Storage-Service_64": "AWS::S3::Bucket",
    "Arch_AWS-Lambda_64": "AWS::Lambda::Function",
    "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance",
    "Arch_AWS-Fargate_64": "AWS::ECS::Cluster"
}

LLM_SUGGESTIONS = {
    # 'AWS::ECS::Cluster': [
    #     'AWS::ECS::TaskDefinition',
    #     'AWS::ECS::Service'
    # ],

    # 'AWS::EC2::VPC': [
    #     'AWS::EC2::InternetGateway',
    #     'AWS::EC2::RouteTable',
    #     'AWS::EC2::Route',
    #     'AWS::EC2::VPCGatewayAttachment',
    #     'AWS::EC2::SubnetRouteTableAssociation'
    # ],

    'AWS::S3::Bucket': [
        'AWS::S3::BucketPolicy'
        ],

    # 'AWS::Lambda::Function': [
    #     'AWS::ApiGateway::RestApi',
    #     'AWS::ApiGateway::Resource',
    #     'AWS::ApiGateway::MethodForLambda',
    #     'AWS::Lambda::Permission'
    # ]
}

# Make directories if they don't exist
input_path = 'testArchitectureDiagrams'
output_path = 'testCFNTemplates'
weight_for_model = "298_icons_best.pt"
architecture_path = "./test"
assert weight_for_model in os.listdir(), "Model Weights missing!"

uri = "mongodb+srv://CapTheStone:VarunVikas@viewme.vzrbu.mongodb.net/?retryWrites=true&w=majority&appName=viewme"
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    print("CONNECTION ERROR!!")
    quit()

db = client['Templates']
icons_collection = db['Templates[PROD]']

# Make directories if they don't exist
os.makedirs(input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

def get_detected_types(result) -> list[str]:
    detected_classes_types = []
    for box in result.boxes: # type: ignore
        class_id = int(box.cls) # Get the class id for the current box
        class_name = model.names[class_id]# Get the class name from the model's names list
        try:
            detected_classes_types.append(CLS_NAME_TO_TYPE[class_name])
        except:
            print(class_name, "not in Mongo yet !!!!")
    return detected_classes_types

def fetch_document_from_mongo(type_name):
    document = icons_collection.find_one({"Type": type_name})
    if not document:
        raise LookupError(f'[{type_name}] does not exist in Database')
    return document

def createNode(type_name) -> Node:
    unit_template = fetch_document_from_mongo(type_name)
    node:Node = Node(type_name, unit_template)
    return node

def get_or_makeNode(type_name, graph:Graph, queue:deque) -> Node:
    if type_name in graph.stored_types:
        dep_node_id = graph.stored_types[type_name][0] # Always chooses first existing node. Need to change with either groups info or something else
        # graph.stored_types[type_name] = graph.stored_types[type_name][1:]+graph.stored_types[type_name][:1] # Left rotate the nodes list of type in graph just so all nodes don't point to same one
        dep_node:Node = graph.nodes[dep_node_id]
    else:
        dep_node:Node = createNode(type_name)
        graph.add_node(dep_node)
        queue.append(dep_node)
    return dep_node

def build_graph_from_types(class_types):
    node_queue = deque()
    graph = Graph()
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
            dep_node = get_or_makeNode(dependency_type, graph=graph, queue=node_queue)
            print(f"Adding Edge for dependency: {dep_node}")

            # Need this..., better way do this would be to remove add edge after LLM suggestion but then we would have to implement
            # singleton resources and since all resources cannot be shared. Like bucketpolicy will be added only once
            # but bucket policies cannot be shared. So since only 1 bucketPolicy is there in queue it will be assinged to one bucket only, but we need
            # 2 policies for each bucket if there are 2 buckets
            if not graph.edge_exists(dep_node, node):
                graph.add_edge(node, dep_node)

        # Add LLM suggestion nodes
        if node.type_name in LLM_SUGGESTIONS:
            for sug_type in LLM_SUGGESTIONS[node.type_name]:
                sug_node = get_or_makeNode(sug_type, graph=graph, queue=node_queue)
                print(f"Adding Edge for LLM suggestion: {sug_node}")
                graph.add_edge(sug_node, node)
    
    return graph

def createName(type_name:str, graph:Graph, type_dict={}):
    type_dict[type_name] = type_dict.get(type_name,0) + 1
    name = 'My'+type_name.split("::")[-1] + str(type_dict[type_name])
    return name

def create_template(result):
    data = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "CloudFormation Template",
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

            # Need to add mapping from node -> dependencies...
            # Bucket -> BucketPolicy ( suggested )
            # BucketPolicy -> Bucket ( Depends )
            # So buckets have mapping to policy, but bucketpolicy needs mapping to buckets
            # So again.... we come back to needing to implement some resouces to be singleton and some to be shared
            # node.replaceMap[graph.nodes[nbr_id].type_name] = createName(graph.nodes[nbr_id].type_name, graph=graph) # Bandaid for now. Wrong cause it messes up numbers
        node.setData(data)

    return data

# Predict using best weights from the model
model = YOLO(weight_for_model)
all_classes = set(range(298))
removed_classes = set([57]) #
allowed_classes = list(all_classes-removed_classes)
results = model.predict(architecture_path, save=True, line_width=1, classes=allowed_classes, conf=0.6)

for i, result in enumerate(results):
    data = create_template(result)
    
    with open(output_path + f"/template{i}.yaml", 'w') as file:
        for k, v in data.items():
            file.write(f"{k}: {v.replace('\\n', '\n  ')}\n")
