from fastapi import FastAPI
from collections import defaultdict, deque
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ClassList(BaseModel):
    file_name: str
    all_types: List[str]

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

    def add_node(self, node:Node):
        self.nodes[node.id] = node
        # if node.type_name in SHAREABLE_RESOURCES:
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
URI = "mongodb+srv://CapTheStone:VarunVikas@viewme.vzrbu.mongodb.net/?retryWrites=true&w=majority&appName=viewme"
icons_collection = None

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

    # suggested_types = get_LLM_types(class_types=class_types)
    # class_types.extend(suggested_types)

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

def create_template(file_name, detected_classes_types):
    data = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": f"CloudFormation Template for {file_name}",
        "Conditions": "",
        "Parameters": "",
        "Resources": "",
        "Outputs": ""
    }

    # Get detected classes
    # detected_classes_types:list[str] = get_detected_types(result)
    graph = build_graph_from_types(detected_classes_types)
    sorted_nodes:list[Node] = graph.topological_sort_out_degree()

    for node in sorted_nodes:
        node_name = createName(node.type_name, graph=graph)
        node.replaceMap[node.type_name] = node_name
        for nbr_id in node.dependency_edges:
            graph.nodes[nbr_id].replaceMap[node.type_name] = node_name
        node.setData(data)

    return data

@app.post("/generateawstemplate")
async def root(all_services: ClassList):
    global icons_collection

    client = connect_to_mongo()
    db = client['Templates']
    icons_collection = db['Templates[PROD]_cleaned']
    return {"message": create_template(all_services.file_name, all_services.all_types)}