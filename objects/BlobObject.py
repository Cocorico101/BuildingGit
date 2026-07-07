from .GitObject import GitObject

class BlobObject(GitObject):
    def __init__(self, data=None):
        self.fmt = b'blob'
        super().__init__(data)

    def init(self):
        self.blobdata = b""

    def serialize(self):
        return self.blobdata


    def deserialize(self, obj):
        self.blobdata = obj
