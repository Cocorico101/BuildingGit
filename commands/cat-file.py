from objects.GitRepo import repo_find, object_read, sha_find
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
    sha = sha_find(repo, args.object, args.type.encode())
    print(f"sha: {sha}")
    found_obj = object_read(repo, sha)
    if found_obj and found_obj.fmt != args.type.encode():
        print("Object not found or type do not match")
        sys.exit(1)
    sys.stdout.buffer.write(found_obj.serialize())
