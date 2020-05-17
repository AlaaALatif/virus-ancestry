import tarfile
from collections import defaultdict
from path import Path
from utils import TreeNode


class TaxData:
    """A class for creating data objects from NCBI Taxonomy databases for
    computing common ancestry between organisms"""

    def __init__(self, data_path: Path):
        """Instantiates an object for the compressed Taxonomy *.tar.gz file"""
        self.data_files = tarfile.open(data_path, 'r')

    def load_data(self):
        """Loads Taxonomy dump into Tree data structure"""
        # map tax ids to names
        self.id2name = defaultdict(str)
        # map names to nodes
        self.name2node = {}
        # map child to parent
        child2parent = {}
        for line in self.data_files.extractfile("names.dmp"):
            row = line.decode().split('\t|\t')
            self.id2name[row[0]] = row[1]
        
        for line in self.data_files.extractfile("nodes.dmp"):
            # parse tab-separated line
            row = line.decode().split('\t|\t')[:-1]
            # grab name and parent name
            name = self.id2name[row[0]]
            parent_name = self.id2name[row[1]]
            child2parent[name] = parent_name
            # create and store a node
            node = TreeNode(name)
            self.name2node[name] = node
        # build classical tree data structure
        for name, node in self.name2node.items():
            if name == "root":
                # initialize root of tree
                self.tree = node
            else:
                # retrieve parent name
                parent_name = child2parent[name]
                # retrieve parent node
                parent_node = self.name2node[parent_name]
                # link child to parent node
                node.parent = parent_node
                # link parent to child node
                parent_node.add_child(node)

    def get_common_ancestor(self, name1, name2):
        """Returns the lowest common ancestor between two organisms
        name1: organism's name or tax id (str or int)
        name2: organism's name or tax id (str or int)"""
        # get lineage of nodes
        node1, node2 = self.name2node[name1], self.name2node[name2]
        lineage1 = node1.get_lineage()
        lineage2 = node2.get_lineage()
        # find 1st common ancestor
        first_common_ancestor = next((p for p in lineage1 if p in set(lineage2)))
        return first_common_ancestor

    def __repr__(self):
        return f'{self.__class__.__name__}: Data Source: {self.data_path}'
