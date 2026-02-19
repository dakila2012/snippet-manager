import argparse
import os
import sys

from db import (
    init_db,
    add_snippet,
    list_snippets,
    search_snippets,
    delete_snippet,
)

parser = argparse.ArgumentParser(
    description="CLI snippet manager for adding, listing, searching, and deleting code snippets stored in a local SQLite database."
)
parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
parser.add_argument("--db", default="~/.snippet_manager/snippets.db", help="Database path (supports ~)")

subparsers = parser.add_subparsers(dest="command", required=True)

# list
subparsers.add_parser("list", help="List all snippets")

# search
search_parser = subparsers.add_parser("search", help="Search snippets")
search_parser.add_argument("query", help="Search term (matches name, lang, or code)")

# add
add_parser = subparsers.add_parser("add", help="Add snippet. Code via stdin.")
add_parser.add_argument("--name", required=True, help="Unique snippet name")
add_parser.add_argument("--lang", required=True, help="Language")

# delete
delete_parser = subparsers.add_parser("delete", help="Delete snippet")
delete_parser.add_argument("name", help="Snippet name")

args = parser.parse_args()

db_path = os.path.expanduser(args.db)
init_db(db_path)

if args.command == "list":
    snippets = list_snippets(db_path)
    if not snippets:
        print("No snippets found.")
    else:
        print("All snippets:")
        for row in snippets:
            print(f"ID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Lang: {row['lang']}")
            print(f"Created: {row['created_at']}")
            print("Code:")
            print(row["code"].rstrip())
            print("=" * 80)
            print()

elif args.command == "search":
    query = args.query.strip()
    if not query:
        print("Error: Provide a non-empty search query.", file=sys.stderr)
        sys.exit(1)
    snippets = search_snippets(db_path, query)
    if not snippets:
        print(f'No snippets matching "{query}".')
    else:
        print(f'Results for "{query}":')
        for row in snippets:
            print(f"ID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Lang: {row['lang']}")
            print(f"Created: {row['created_at']}")
            print("Code:")
            print(row["code"].rstrip())
            print("=" * 80)
            print()

elif args.command == "add":
    name = args.name.strip()
    lang = args.lang.strip()
    if not name or not lang:
        print("Error: Name and language must be non-empty.", file=sys.stderr)
        sys.exit(1)
    code = sys.stdin.read()
    if not code.strip():
        print("Error: Provide non-empty code via stdin.", file=sys.stderr)
        sys.exit(1)
    if add_snippet(db_path, name, lang, code):
        print(f'Added "{name}".')
    else:
        print(f'Error: "{name}" already exists.', file=sys.stderr)
        sys.exit(1)

elif args.command == "delete":
    name = args.name.strip()
    if not name:
        print("Error: Provide a non-empty name.", file=sys.stderr)
        sys.exit(1)
    if delete_snippet(db_path, name):
        print(f'Deleted "{name}".')
    else:
        print(f'"{name}" not found.', file=sys.stderr)
        sys.exit(1)
