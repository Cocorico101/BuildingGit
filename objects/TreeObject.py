from .GitObject import GitObject

class TreeNode(object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha

class TreeObject(GitObject):
    fmt = b'tree'
    def init(self):
        self.tree_data = []

    def serialize(self):
        return tree_serialize(self)


    def deserialize(self, obj):
        self.tree_data = tree_deserialize(obj)

def tree_leaf_sort_key(leaf):
    # Append the / if its a directory
    if leaf.mode.startswith(b'04'):
        return leaf.path + "/"
    return leaf.path


def tree_serialize(tree_obj):
    tree_obj.sort(key=tree_leaf_sort_key)
    raw = b""
    for node in tree_obj.tree_data:
        mode, path, sha = node.mode, node.path, node.sha
        raw += mode + b" " + path.encode("utf8") + b'\x00' 
        # Convert hex to binary
        raw_sha = bytes.fromhex(sha)
        raw += raw_sha
    return raw

def tree_deserialize(raw):
    data = []
    i = 0
    length = len(raw)
    while i < length:
        new_idx, parsed = tree_deserialize_one(raw, i)
        i = new_idx
        data.append(parsed)
    return data


def tree_deserialize_one(raw, start=0):
    # Parse for the mode
    space_idx = raw.find(b' ', start)
    file_mode = raw[start:space_idx]
    # Make sure the mode is 5 or 6 bytes
    assert space_idx - start == 5 or space_idx - start == 6
    # Normalize it all to 6 bytes
    if len(file_mode) == 5:
        file_mode = b"0" + file_mode

    # Parse for the path
    null_idx = raw.find(b'\x00', space_idx)
    path = raw[space_idx+1: null_idx]
    # Convert sha 20 bytes of binary into lowercase hex
    sha = raw[null_idx+1:null_idx+21].hex()

    return (null_idx+21, TreeNode(file_mode, path.decode("utf8"), sha))
