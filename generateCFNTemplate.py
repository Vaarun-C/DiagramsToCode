import os
import yaml
from ultralytics import YOLO
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict, deque
import json

class Node:
    ID = 0  # Static variable to assign unique IDs to each node

    def __init__(self, type_name, parameters='', resources='', outputs='', dependencies=None):
        self.id = Node.ID
        Node.ID += 1
        self.type_name = type_name
        self.parameters = parameters
        self.resources = resources
        self.outputs = outputs
        self.dependencies = [] if dependencies is None else dependencies # dependency types
        self.dependency_edges = []  # Stores IDs of dependent nodes
        self.replaceMap = {}


    def __repr__(self):
        return f"Node(type_name={self.type_name}, id={self.id})"


class Graph:
    def __init__(self):
        self.nodes:dict[int,Node] = {} # ID -> Node
        self.stored_types:dict[str,list[int]] = {} # type -> list[ID]
        self.in_degree = defaultdict(int)

    def add_node(self, node:Node):
        self.nodes[node.id] = node
        self.stored_types.get(node.type_name, []).append(node.id)

    def add_edge(self, from_node:Node, to_node:Node):
        """adds the edge in the reverse direction"""
        to_node.dependency_edges.append(from_node.id)
        self.in_degree[from_node.id] += 1

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
    "Arch_Amazon-RDS_64": "AWS::RDS::DBInstance"
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

def get_or_makeNode(type_name, graph:Graph, queue:deque) -> Node:
    if type_name in graph.stored_types:
        dep_node_id = graph.stored_types[type_name]
        dep_node:Node = graph.nodes[dep_node_id]
    else:
        unit_template = fetch_document_from_mongo(type_name)
        dep_node:Node = Node(type_name,
            parameters=unit_template.get("Parameters"),
            resources=unit_template.get("Parameters"),
            outputs=unit_template.get("Outputs"),
            dependencies=unit_template.get("Dependencies"),
        )
        graph.add_node(dep_node)
        queue.append(dep_node)
    return dep_node

def build_graph_from_types(class_types):
    node_queue = deque()
    graph = Graph()
    for class_type in class_types:
        unit_template = icons_collection.find_one({"Type": class_type})
        if not unit_template:
            print(f"No additional details found for class {class_type}")
            continue
        node = Node(class_type,
            parameters=unit_template.get("Parameters"),
            resources=unit_template.get("Parameters"),
            outputs=unit_template.get("Outputs"),
            dependencies=unit_template.get("Dependencies"),
        )
        graph.add_node(node)
        node_queue.append(node)
    
    while node_queue:
        node:Node = node_queue.popleft()
        for dependency_type in node.dependencies:
            dep_node = get_or_makeNode(dependency_type, graph=graph, queue=node_queue)
            graph.add_edge(node, dep_node)
    
    return graph

def createName(type_name:str, graph:Graph, type_dict={}):
    type_dict[type_name] = type_dict.get(type_name,0) + 1
    name = 'My'+type_name.split("::")[-1] + str(type_dict[type_name])
    return name

def create_template(result):
    data = {
        "AWSTemplateFormatVersion": '2010-09-09',
        "Description": "CloudFormation Template",
        "Parameters": '',
        "Resources": '',
        "Outputs": ''
    }

    # Get detected classes
    detected_classes_types:list[str] = get_detected_types(result)
    
    graph = build_graph_from_types(detected_classes_types)
    
    sorted_nodes:list[Node] = graph.topological_sort_out_degree()
    print(sorted_nodes)
    input()
    for node in sorted_nodes:
        node_name = createName(node.type_name, graph=graph)
        node.replaceMap[node.type_name] = node_name
        for nbr_id in node.dependency_edges:
            graph.nodes[nbr_id].replaceMap[node.type_name] = node_name
        
        for i, dep_type in enumerate(node.dependencies):
            dep_name = node.replaceMap[dep_type]
            node_parameters = node.parameters or ''
            node_resources = node.resources or ''
            node_outputs = node.outputs or ''
            node_parameters.replace(f'$${i + 2}', dep_name)
            node_resources.replace(f'$${i + 2}', dep_name)
            node_outputs.replace(f'$${i + 2}', dep_name)

        node_parameters.replace('$$1', node_name)
        node_resources.replace('$$1', node_name)
        node_outputs.replace('$$1', node_name)

        data['Parameters'] += node_parameters
        data['Resources'] += node_resources
        data['Outputs'] += node_outputs

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
        yaml.dump(data, file, default_flow_style=False)  # default_flow_style=False makes the output more readable

    with open(output_path + f"/template{i}.json", 'w') as file:
        file.write(json.dumps(data, indent=4))