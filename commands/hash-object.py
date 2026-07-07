from objects.GitRepo import repo_find, object_write
from objects.GitObjectFactory import object_create
import sys

def register(subparsers):
    """
    wyag hash-object -w TYPE PATH

    """
    argsp = subparsers.add_parser("hash-object", help="Computes hash of a file and store it in the repo")
    argsp.add_argument("-w",
                       action='store_true',
                       help="Writes the object to the database.")   
    argsp.add_argument("type",
                       metavar="type",
                       help="Type of object to hash.")
 
    argsp.add_argument("path",
                       metavar="path",
                       help="The path to read the <file> from.")         
    argsp.set_defaults(func=cmd_hash_object)

def cmd_hash_object(args):
    """
    Display the contents of the object
    """
    # Go to the file path
    repo = repo_find()
    with open (args.path, 'rb') as file:
        data = file.read()
    obj = object_create(args.type.encode(), data)
    # Call object_write to compute the sha
    print(object_write(repo, obj))
