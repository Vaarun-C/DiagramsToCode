from collections import defaultdict, deque
from Node import Node

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
