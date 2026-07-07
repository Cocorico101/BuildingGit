from objects.GitRepo import repo_find, object_read, object_find
import sys

def register(subparsers):
    """
    wyag cat-file TYPE OBJECT

    """
    argsp = subparsers.add_parser("cat-file", help="Display contents of an object in STDOUT")
    argsp.add_argument("type",
                       metavar="type",
                       help="Type of object to display.")
    argsp.add_argument("object",
                       metavar="object",
                       help="The object to display contents.")         
    argsp.set_defaults(func=cmd_cat_file)

def cmd_cat_file(args):
    """
    Display the contents of the object
    """
    repo = repo_find()
    # TODO: Reimplement object_find appropriately based on the object type after
    found_obj = object_find(repo, args.type.encode(), args.object)
    print(f"Object {args.object}")
    sys.stdout.buffer.write(object_read(repo, args.object).serialize())
