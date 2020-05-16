class Node:
    def __init__(self, name: str, parent_name: str):
        self.name = name
        self.parent = parent_name

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} -> {self.parent}'
