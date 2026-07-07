from objects.GitRepo import repo_find, object_find, object_read


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
    found_obj = object_find(repo, args.type.encode(), args.object)
    sys.stdout.buffer.write(object_read(repo, found_obj).serialize())
