import hashlib
import os
import zlib
from .GitObjectFactory import object_create
from .GitRepo import repo_file


def object_read(repo, sha):
    """
    Read object based on its sha
    """

    # Find the path based on its sha
    # First two is the directory + filename as the remaining
    path = repo_file(repo, "objects", sha[:2], sha[2:])
    # Return None if path doesn't exist
    if not path or not os.path.isfile(path):
        return None
    # Read the file at that path in binary format + decompress via zlib
    with open(path, 'rb') as file:
        binary_data = file.read()

    decompressed = zlib.decompress(binary_data)
    # Extract the object TYPE
    obj_type_idx = decompressed.find(b' ')
    obj_type = decompressed[:obj_type_idx]

    # Extract the object SIZE
    obj_size_idx = decompressed.find(b'\x00')
    obj_size = int(decompressed[obj_type_idx+1:obj_size_idx].decode("ascii"))
    # Exclude the header and compare the data size vs actual decompressed data length
    if obj_size != (len(decompressed)-obj_size_idx-1):
        return None
    #Call the appropriate constructor based on the obj type
    return object_create(obj_type, decompressed[obj_size_idx+1:])
    

def object_write(repo, obj):
    """
    Compute sha based on the path
    """
    # Write the type
    data = obj.serialize()
    payload = obj.fmt + b' ' +  str(len(data)).encode() + b'\x00' + data

    # Compute the sha
    sha = hashlib.sha1(payload).hexdigest()
    # Compute the path
    if repo:
        path = repo_file(repo, "objects", sha[:2], sha[2:], mkdir=True)
        if not os.path.exists(path):
            with open(path, 'wb') as file:
                file.write(zlib.compress(payload))
    return sha