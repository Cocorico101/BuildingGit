from objects.GitRepo import repo_find, object_read, object_find



def register(subparsers):
    argsp = subparsers.add_parser("log", help="Display the history of a given commit")
    argsp.add_argument("commit",
                       nargs="?",
                       default="HEAD",
                       help="The commit to display the history.")
    argsp.set_defaults(func=cmd_log)

def cmd_log(args):
    """
    Display the history of the commit
    """
    repo = repo_find()
    print(f" args.commit: {args.commit}")
    found_obj = object_find(repo, args.commit)
    seen = set()
    print(f"repo: {repo}")
    log_graphviz(repo, found_obj, seen)


def log_graphviz(repo, sha, seen):
    """
    Display the commit history
    """
    if not sha or sha in seen:
        return

    # Track cycles
    seen.add(sha)
    # Find the commit object
    commit = object_read(repo, sha)

    # Assert to make sure the sha points to a commit
    assert commit.fmt == b'commit'
        
    # Base case
    if b'parent' not in commit.commitdata:
        return

    # Display the commit messages - human readable
    message = commit.commitdata[None].decode("utf8").strip()
    print(f"message {message}")
    # Escape special characters
    message = message.replace("\\", "\\\\")
    message = message.replace("\"", "\\\"")
    # Only display the first line of the message
    if '\n' in message:
        message = message[:message.index('\n')]
    print(f"  c_{sha} [label=\"{sha[0:7]}: {message}\"]")

    
    # Recursive case - traverse the parents
    parents = commit.commitdata[b'parent']
    if type(parents) != list:
        parents = [parents]
    for p in parents:
        # parent value is commit hash in hex, which is ascii
        p = p.decode('ascii')
        print (f"  c_{sha} -> c_{p};")
        log_graphviz(repo, p, seen)
