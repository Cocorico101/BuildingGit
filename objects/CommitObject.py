from .GitObject import GitObject

class CommitObject(GitObject):
    def __init__(self, data=None):
        self.fmt = b'commit'
        super().__init__(data)

    def init(self):
        self.commitdata = b""

    def serialize(self):
        return self.commitdata


    def deserialize(self, obj):
        self.commitdata = obj
