from .GitObject import GitObject

class TreeObject(GitObject):
    def __init__(self, data=None):
        self.fmt = b'tree'
        super().__init__(data)

    def init(self):
        self.treedata = b""

    def serialize(self):
        return self.treedata


    def deserialize(self, obj):
        self.treedata = obj
