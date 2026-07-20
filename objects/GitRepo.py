import configparser
import os
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

