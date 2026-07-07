from objects.GitRepo import repo_create


def register(subparsers):
    argsp = subparsers.add_parser("init", help="Initialize a new, empty repository")
    argsp.add_argument("path",
                       metavar="directory",
                       nargs="?",
                       default=".",
                       help="Where to create the repository.")
    argsp.set_defaults(func=cmd_init)

def cmd_init(args):
    #create a repo
    repo_create(args.path)