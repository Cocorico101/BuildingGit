from .BlobObject import BlobObject
from .CommitObject import CommitObject

class GitObjectFactory:
    TYPE_TO_CONSTRUCTOR = {
        b"blob": BlobObject,
        b"commit": CommitObject,
        b"tree": TreeObject,
        # b"tag": TagObject,
    }

    @classmethod
    def get_constructor(cls, obj_type):
        if obj_type not in cls.TYPE_TO_CONSTRUCTOR:
            raise ValueError(f"Unknown git object type: {obj_type}")
        return cls.TYPE_TO_CONSTRUCTOR[obj_type]


def object_create(obj_type, data):
    """
    Create the object based on types
    """

    constructor = GitObjectFactory.get_constructor(obj_type)
    return constructor(data)


