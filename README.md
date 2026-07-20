# BuildingGit

BuildingGit is a learning project that implements a small subset of Git in Python.
It is inspired by wyag and focuses on core object storage and basic history traversal.

This is not a full replacement for Git. The goal is to understand how Git internals work.

## Features Implemented

- Repository initialization
- Object hashing and object writes
- Object content display (cat-file)
- Tree object listing (ls-tree) with recursion support
- Commit history traversal output in DOT format (for Graphviz)
- Full SHA-1 hash lookup
- HEAD and symbolic ref resolution

## Features NOT Yet Implemented

- Short hash lookup (e.g., first 7 characters)
- Branch name resolution (e.g., `master`, `main`)
- Tag resolution
- Full branch and tag listing commands

## Project Layout

- cores/wyag: CLI entrypoint script
- cores/libwyag.py: argparse and command registration
- commands/: command handlers (`init`, `hash-object`, `cat-file`, `log`, `ls-tree`)
- objects/GitRepo.py: repository discovery and filesystem helpers
- objects/GitObjectStore.py: low-level object read/write + zlib storage
- objects/Refs.py: symbolic ref and SHA resolution
- objects/GitObjectFactory.py: object type to constructor mapping
- objects/*.py: object models (`BlobObject`, `TreeObject`, `CommitObject`)

## Requirements

- Python 3
- Graphviz (optional, only needed for rendering commit history diagrams)

Install Graphviz on Ubuntu or WSL:

sudo apt-get update
sudo apt-get install graphviz

## Usage

Run commands from the repository root.

General format:

cores/wyag <command> [arguments]

### 1) Initialize a Repository

cores/wyag init [path]

Examples:

cores/wyag init
cores/wyag init my-repo

### 2) Hash an Object

cores/wyag hash-object [-w] <type> <path>

- type is usually blob in current usage
- -w writes the object into .git/objects

Example:

cores/wyag hash-object -w blob README.md

### 3) Show Object Contents

cores/wyag cat-file <type> <object_sha>

Example:

cores/wyag cat-file blob <sha>

Notes:

- `cat-file` validates object type before printing
- interactive terminal output keeps prompts readable with a trailing newline when needed

### 4) Show Commit History as DOT

cores/wyag log <commit_sha>

This prints Graphviz DOT text to stdout.

Save it to a file:

cores/wyag log <commit_sha> > log.dot

Render PDF:

dot -Tpdf log.dot -o log.pdf

Or do it in one pipeline:

cores/wyag log <commit_sha> | dot -Tpdf -o log.pdf

### 5) List Tree Contents

cores/wyag ls-tree [-r] <tree_sha>

Examples:

cores/wyag ls-tree <tree_sha>
cores/wyag ls-tree -r <tree_sha>

## Notes About log

- log currently traverses commit parents recursively.
- Node labels include short SHA and a sanitized single-line commit message.
- Special characters in commit messages are escaped for DOT safety.
- Invalid input now fails cleanly with a user-facing error message.

## Current Limitations

- `hash-object` currently writes objects when a repo is found, even if `-w` is omitted.
- SHA resolution accepts full 40-character hashes and symbolic refs; short hash disambiguation is not implemented.
- Error handling is still being standardized across all commands.

## Learning Goals

The good next milestones are:

1. Implement proper ref resolution for HEAD and branch names.
2. Add short SHA lookup with ambiguity checks.
3. Add checkout, commit, and tree walking commands.
4. Add unit tests for parser, object storage, and command behavior.
