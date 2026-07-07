from .GitObject import GitObject

class BlobObject(GitObject):
    def __init__(self):
        fmt = b'blob'

    def serialize(self):
        return self.blobdata


    def deserialize(self, obj):
        self.blobdata = obj
