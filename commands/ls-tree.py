from objects.GitRepo import repo_find, object_read, object_find
import sys

def register(subparsers):
    """
    wyag ls-tree -r TREE

    """
    argsp = subparsers.add_parser("cat-file", help="Display contents of an object in STDOUT")
    argsp.add_argument("-r",
                       dest="recursive",
                       action='store_true',
                       help="Recurses into subtree.")   
    argsp.add_argument("tree",
                       metavar="tree",
                       help="Tree like object.")    
    argsp.set_defaults(func=cmd_ls_tree)

def cmd_ls_tree(args):
    """
    Display the contents of the object
    """
    repo = repo_find()
    # TODO: Reimplement object_find appropriately based on the object type after
    ls_tree(repo, args.tree, args.recursive)
    

def ls_tree(repo, ref, recursive=None, prefix=""):
    # Find sha based on arguments
    sha = object_find(repo, ref, b'tree')
    # Return tree object based on sha
    found_obj = object_read(repo, sha)
    # Display tree object contents based on mode

    # If recursive is true, then do the recursion, otherwise, print out contents


