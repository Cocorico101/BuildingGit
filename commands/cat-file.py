from objects.GitRepo import repo_find
from objects.GitObjectStore import object_read
from objects.Refs import sha_find
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
    if not sha:
        print(f"Error: Object {args.object} not found or type mismatch", file=sys.stderr)
        sys.exit(1)
    found_obj = object_read(repo, sha)
    data = found_obj.serialize()
    sys.stdout.buffer.write(data)

    # Keep shell prompts readable without changing piped output behavior.
    if sys.stdout.isatty() and (len(data) == 0 or data[-1] != 0x0A):
        sys.stdout.write("\n")
