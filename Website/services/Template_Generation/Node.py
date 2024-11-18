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
