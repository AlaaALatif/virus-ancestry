class TreeNode:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = set()
        
    def add_child(self, child_node):
        "Adds a child node"
        self.children.add(child_node)
        
    def get_lineage(self):
        "Returns a list of the node's ancestors"
        return [node for node in self.iter_lineage()]
        
    def iter_lineage(self):
        "An iterator over a node's ancestors"
        node = self
        while node.parent:
            yield node.parent
            node = node.parent

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} -> {[c.name for c in self.children]}'