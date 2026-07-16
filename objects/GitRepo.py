import os
import configparser
import re
import zlib
import hashlib
from .GitObjectFactory import object_create

class GitRepository:
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir =  os.path.join(path, ".git")

        # Read the config file in .gitdir/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        # Check if the path exist and if its a file
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
def repo_path(repo, *path):
    """
    General path building function
    """
    return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path, mkdir=False):
    """
    Return and optionally create a path to a file. 
    Creates directory up until the last component
    """
    dir_path = repo_dir(repo, *path[:-1], mkdir=mkdir)
    if dir_path:
        return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
    """
    Return and optionally create a path to a directory
    """
    path = repo_path(repo, *path)
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception (f"{path} is not a directory")
    elif mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_default_config():
    """
    Fills out default config file
    """
    config = configparser.ConfigParser()
    config.add_section("core")
    config.set("core", "repositoryformatversion", "0" )
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false" )
    return config

def repo_find(path="."):
    """
    Function that returns the root of the current repo
    """
    #Base case:
    #Grab the fully resolved path
    full_path = os.path.realpath(path)
    # If path has .git, then it is a repo that we want
    if os.path.isdir(os.path.join(full_path, ".git")):
        return GitRepository(path)
    
    #Recursive case:
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        return None
    return repo_find(parent)



def repo_create(path):
    """
    Helper function to creates the repo based on the path
    """
    repo = GitRepository(path, True)

    # If the path exists
    if os.path.exists(repo.worktree):
        # not a directory
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty")
        
    else:
        os.makedirs(repo.worktree)

    # write git description
    with open(repo_file(repo, "description", mkdir=True), 'w') as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # write git HEAD
    with open(repo_file(repo, "HEAD", mkdir=True), 'w') as f:
        f.write("ref: refs/heads/master\n")
    # write config file
    with open(repo_file(repo, "config", mkdir=True), 'w') as f:
        config = repo_default_config()
        config.write(f)

    return repo

def object_read(repo, sha):
    """
    Read object based on its sha
    """

    # Find the path based on its sha
    # First two is the directory + filename as the remaining
    path = repo_file(repo, "objects", sha[:2], sha[2:])
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
            
def sha_find(repo, name, fmt=None, follow=True):
    """
    If name is HEAD: resolve to .git/HEAD
    If name is a full hash, hash is returned unmodified    
    Returns sha, or None if type validation fails
    """
    sha = None
    pattern = r"^[a-zA-Z0-9]{40}$"
    if name == 'HEAD':
        sha = ref_find(repo, name)
    elif re.match(pattern, name):
        sha = name
    else:
        # Try as a ref (branch name)
        sha = ref_find(repo, name)

    # Validate type if requested
    if sha and fmt:
        obj = object_read(repo, sha)
        if obj and obj.fmt != fmt:
            return None
    
    return sha

def ref_find(repo, ref):
    """
    Symbolic link ref: refs/remotes/origin/master
    Returns the sha associated with the ref
    """
    # A path to a file
    path = repo_file(repo, ref)
    # Base case
    if not os.path.isfile(path):
        return None
    # Read the file to grab the contents
    with open(path, 'r') as fp:
        data = fp.read()[:-1]


    # If the file does not contain SHA1 hash, keep recursing
    if data.startswith("ref: "):
        return ref_find(repo, data[5:])
    return data

