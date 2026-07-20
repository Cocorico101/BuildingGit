from objects.GitRepo import repo_find
from objects.GitObjectStore import object_read
from objects.Refs import sha_find
import sys


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
    sha = sha_find(repo, args.commit)
    if not sha:
        print(f"Error: Commit {args.commit} not found", file=sys.stderr)
        sys.exit(1)

    obj = object_read(repo, sha)
    if not obj or obj.fmt != b'commit':
        print(f"Error: {args.commit} is not a commit", file=sys.stderr)
        sys.exit(1)

    seen = set()
    print("digraph wyaglog {")
    print("  node [shape=rect];")
    log_graphviz(repo, sha, seen)
    print("}")


def log_graphviz(repo, sha, seen):
    """
    Display the commit history
    """
    if not sha or sha in seen:
        return

    # Track cycles
    seen.add(sha)
    # Find the commit object
    commit_obj = object_read(repo, sha)

    # Skip invalid nodes defensively; cmd_log does the user-facing validation.
    if not commit_obj or commit_obj.fmt != b'commit':
        return
        
    # Display the commit messages - human readable
    message = commit_obj.commitdata.get(None, b"").decode("utf8", errors="replace")
    message = " ".join(message.splitlines()).strip()
    # Escape special characters
    message = message.replace("\\", "\\\\")
    message = message.replace("\"", "\\\"")
    print(f"  c_{sha} [label=\"{sha[0:7]}: {message}\"];")

    # Base case
    if b'parent' not in commit_obj.commitdata:
        return

    
    # Recursive case - traverse the parents
    parents = commit_obj.commitdata[b'parent']
    if type(parents) != list:
        parents = [parents]
    for p in parents:
        # parent value is commit hash in hex, which is ascii
        p = p.decode('ascii')
        print(f"  c_{sha} -> c_{p};")
        log_graphviz(repo, p, seen)
