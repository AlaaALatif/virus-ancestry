import tarfile
from collections import defaultdict
from path import Path
from utils import Node


class TaxData:
    """A class for creating data objects from NCBI Taxonomy databases for
    computing common ancestry between organisms"""

    def __init__(self, data_path: Path):
        """Instantiates an object for the compressed Taxonomy *.tar.gz file"""
        self.data_files = tarfile.open(data_path, 'r')

    def load_data(self):
        """Loads Taxonomy dump into suitable data structures
        self.id2name: dictionary that maps tax ids to organism names
        self.name2node: dictionary that maps organism names to corresponding
        nodes"""
        # map tax ids to names
        self.id2name = defaultdict(str)
        for line in self.data_files.extractfile("names.dmp"):
            row = line.decode().split('\t|\t')
            self.id2name[row[0]] = row[1]
        # map names to nodes
        self.name2node = {}
        for line in self.data_files.extractfile("nodes.dmp"):
            # parse tab-separated line
            row = line.decode().split('\t|\t')[:-1]
            # grab name and parent name
            name = self.id2name[row[0]]
            parent_name = self.id2name[row[1]]
            # create and store a node
            node = Node(name, parent_name)
            self.name2node[name] = node
        return 'Data Sucessfully Loaded into RTree'

    def get_common_ancestor(self, name1, name2):
        """Returns the lowest common ancestor between two organisms
        name1: organism's name or tax id (str or int)
        name2: organism's name or tax id (str or int)"""
        # get lineage of nodes
        if type(name1) == int:
            name1 = self.id2name[name1]
        if type(name2) == int:
            name2 = self.id2name[name2]
        lineage1 = self.get_lineage(name1)
        lineage2 = self.get_lineage(name2)
        # find 1st common ancestor
        first_common_ancestor = next((p for p in lineage1 if p in set(lineage2)))
        return first_common_ancestor

    def get_lineage(self, name: str):
        """Returns the full lineage of an organism
        name: organism's name
        self.lineage: organism's lineage (list)"""
        node = self.name2node[name]
        self.lineage = []
        self.lineage = self._get_lineage(node)
        return self.lineage

    def _get_lineage(self, node: Node):
        """Helper function to recursively traverse data structure and get
        lineage"""
        self.lineage.append(node.name)
        if node.name == 'root':
            return self.lineage
        return self._get_lineage(self.name2node[node.parent])

    def __repr__(self):
        return f'{self.__class__.__name__}: Data Source: {self.data_path}'
