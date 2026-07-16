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
- Commit object traversal via refs

## Project Layout

- cores/wyag: CLI entrypoint script
- cores/libwyag.py: argparse and command registration
- commands/: command handlers (init, hash-object, cat-file, log)
- objects/: repository and object model code

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

### 4) Show Commit History as DOT

cores/wyag log <commit_sha>

This prints Graphviz DOT text to stdout.

Save it to a file:

cores/wyag log <commit_sha> > log.dot

Render PDF:

dot -Tpdf log.dot -o log.pdf

Or do it in one pipeline:

cores/wyag log <commit_sha> | dot -Tpdf -o log.pdf

## Notes About log

- log currently traverses commit parents recursively.
- Node labels include short SHA and first line of commit message.
- Special characters in commit messages are escaped for DOT safety.

## Current Limitations

- object_find currently returns the provided name directly and does not fully resolve references (for example HEAD to refs/heads/... to SHA).
- cat-file currently reads args.object directly instead of using the resolved value from object_find.
- Type validation and object resolution behavior are still minimal.

## Learning Goals

The good next milestones are:

1. Implement proper ref resolution for HEAD and branch names.
2. Improve object_find to support short SHA lookup and ambiguity checks.
3. Add checkout, commit, and tree walking commands.
4. Add unit tests for parser and object resolution behavior.
