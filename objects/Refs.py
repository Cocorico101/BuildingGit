import re
import os
from .GitRepo import repo_file
from .GitObjectStore import object_read

def sha_find(repo, name, fmt=None, follow=True):
    """
    If name is HEAD: resolve to .git/HEAD
    If name is a full hash, hash is returned unmodified    
    sha, or None if type validation fails
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
        if not obj or obj.fmt != fmt:
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