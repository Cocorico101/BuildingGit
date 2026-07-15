from objects.GitRepo import repo_find, object_read, object_find
import sys,os

def register(subparsers):
    """
    wyag ls-tree -r TREE

    """
    argsp = subparsers.add_parser("ls-tree", help="Display contents of a TREE object in STDOUT")
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
    

def get_obj_type_based_on_mode(mode):
    obj_type = ""
    match mode:
        case b'04': 
            obj_type = 'tree'
        case b'10':
            obj_type = 'blob'
        case b'12':
            obj_type = 'blob'
        case b'16':
            obj_type = 'commit'
    return obj_type

def ls_tree(repo, ref, recursive=None, prefix=""):
    # Find sha based on arguments
    sha = object_find(repo, ref, b'tree')
    # Return tree object based on sha
    found_obj = object_read(repo, sha)
    # Display tree object contents based on mode
    for node in found_obj.tree_data:
        mode = b'00' #placeholder
        if len(node.mode) == 5:
            mode = node.mode[0:1]
        else:
            mode = node.mode[0:2]

        obj_type = get_obj_type_based_on_mode(mode)
        #if not recursion and leaf node:
        if obj_type != 'tree' or not recursive:
            print(f"{node.mode.decode('ascii')} {obj_type} {node.sha} {os.path.join(prefix,node.path)}")
        else:
            ls_tree(repo, node.sha, recursive, os.path.join(prefix,node.path))



