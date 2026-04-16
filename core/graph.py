# core/graph.py

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def remove_node(self, node):
        # Remove all edges connected to this node
        edges_to_remove = []
        for edge in self.edges:
            if edge.source == node or edge.target == node:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.edges.remove(edge)
        # Remove the node
        self.nodes.remove(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def remove_edge(self, edge):
        self.edges.remove(edge)
    
    def get_edges_for_node(self, node):
        return [edge for edge in self.edges if edge.source == node or edge.target == node]
    
    def clear(self):
        self.nodes.clear()
        self.edges.clear()