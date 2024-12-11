from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Node import Node
from Graph import Graph
from collections import deque

class template_generator:
    def __init__(self) -> None:    
        self.SHAREABLE_RESOURCES = {
            'AWS::EC2::VPC',
            'AWS::EC2::Subnet',
            'AWS::EC2::InternetGateway',
            'AWS::EC2::VPCGatewayAttachment',
            'AWS::EC2::RouteTable',
            'AWS::EC2::Route',
            'AWS::DynamoDB::Table',
            'AWS::ECS::Cluster',
            'AWS::ApiGateway::RestApi',
            'AWS::IAM::RoleForLambda',
            'AWS::IAM::RoleForEMRService',
            'AWS::IAM::RoleForEMRInstance',
            'AWS::IAM::RoleForGlueService',
            'AWS::IAM::RoleForMWAA',
            'AWS::IAM::RoleForAppSyncService',
            'AWS::IAM::RoleForStepFunctionExecution',
            'AWS::IAM::RoleForBedrock',
            'AWS::IAM::RoleForComprehend',
            'AWS::IAM::RoleForKendraExecution',
            'AWS::IAM::RoleForLexExecution',
            'AWS::IAM::RoleForPollyExecution',
            'AWS::IAM::RoleForSageMakerExecution',
            'AWS::IAM::RoleForTextractExecution',
            'AWS::IAM::RoleForTranscribeExecution',
            'AWS::IAM::RoleForBatchService',
            'AWS::IAM::RoleForBatchInstance',
            'AWS::IAM::RoleForEKSCluster',
            'AWS::IAM::RoleForEKSNodeGroup',
            'AWS::IAM::RoleForPrometheusWrite',
            'AWS::IAM::RoleForPrometheusQuery'
        }
        self.URI = "mongodb+srv://CapTheStone:VarunVikas@viewme.vzrbu.mongodb.net/?retryWrites=true&w=majority&appName=viewme&tlsAllowInvalidCertificates=true"

        # Connect to MongoDB
        try:
            self.client = MongoClient(self.URI, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            print("CONNECTION ERROR!!")
            quit()

        db = self.client['Templates']
        self.icons_collection = db['Templates[PROD]_cleaned']

    def fetch_document_from_mongo(self, type_name: str):
        document = self.icons_collection.find_one({"Type": type_name})
        if not document:
            raise LookupError(f'[{type_name}] does not exist in Database')
        return document

    def createNode(self, type_name:str) -> Node:
        unit_template = self.fetch_document_from_mongo(type_name)
        node:Node = Node(type_name, unit_template)
        return node

    def get_or_makeNode(self, type_name: str, dep_type_name: str, graph: Graph, queue: deque) -> Node:
        if (len(graph.stored_types.get(dep_type_name, [])) == 0):
            dep_node:Node = self.createNode(dep_type_name)
            graph.add_node(dep_node)
            queue.append(dep_node)
        else:
            # Always chooses first existing node. Need to change with either groups info or something else
            candidate_dep_node_ids = graph.stored_types[dep_type_name]
            if dep_type_name in self.SHAREABLE_RESOURCES:
                dep_node_id = candidate_dep_node_ids[0] 
            else: 
                # dep_type_name in Unique
                for candidate_node_id in candidate_dep_node_ids:
                    candidate_node = graph.nodes[candidate_node_id]
                    if type_name not in candidate_node.consumedBy:
                        candidate_node.consumedBy.add(type_name)
                        dep_node_id = candidate_node_id
                        break
                else:
                    dep_node:Node = self.createNode(dep_type_name)
                    graph.add_node(dep_node)
                    queue.append(dep_node)
                    dep_node_id = dep_node.id
            dep_node:Node = graph.nodes[dep_node_id]
        return dep_node

    def build_graph_from_types(self, class_types:list[str]) -> Graph:
        node_queue = deque()
        graph = Graph()

        for class_type in class_types:
            try:
                node:Node = self.createNode(class_type)
                graph.add_node(node)
                node_queue.append(node)
            except LookupError as e:
                print(f"No additional details found for class {class_type}", e)
        
        while node_queue:
            node:Node = node_queue.popleft()
            # print(f"Creating Node for: {node}")
            # Add dependency nodes
            for dependency_type in node.dependencies:
                dep_node = self.get_or_makeNode(node.type_name, dependency_type, graph=graph, queue=node_queue)
                # print(f"Adding Edge for dependency: {dep_node}")
                graph.add_edge(node, dep_node)

        ids_to_remove = []
        for id, node in graph.nodes.items():
            if (node.type_name in self.SHAREABLE_RESOURCES) and (len(node.dependency_edges) == 0):
                ids_to_remove.append(id)

        new_nodes = {}
        for id, node in graph.nodes.items():
            if (id in ids_to_remove):
                continue
            new_nodes[id] = graph.nodes[id]

        graph.nodes = new_nodes
        return graph

    def createName(self, type_name:str, graph:Graph) -> str:
        graph.type_dict[type_name] = graph.type_dict.get(type_name,0) + 1
        name = 'My'+''.join(type_name.split("::")[-2:]) + str(graph.type_dict[type_name])
        return name

    def create_template(self, file_name: str, detected_classes_types: list[str]) -> dict:
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
        graph = self.build_graph_from_types(detected_classes_types)
        # sorted_nodes:list[Node] = graph.topological_sort_out_degree()
        sorted_nodes = graph.nodes.values()
        for node in sorted_nodes:
            node_name = self.createName(node.type_name, graph=graph)
            node.replaceMap[node.type_name] = node_name
            for nbr_id in node.dependency_edges:
                graph.nodes[nbr_id].replaceMap[node.type_name] = node_name
        for node in sorted_nodes:
            node.setData(data)

        return data