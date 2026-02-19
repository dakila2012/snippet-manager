# snippet-manager

A CLI snippet manager for developers to store, organize, and retrieve code snippets in a local SQLite database. Supports core CRUD operations via intuitive subcommands: add snippets (with stdin for multiline code), list all snippets, search by keyword across name/language/code, and delete by name. Features unique names, timestamps, and fuzzy partial matching for efficient workflow.

Production-ready with excellent UX, no external dependencies, and robust error handling.

## Installation

bash
git clone <repo-url>
cd snippet-manager
No external dependencies (uses Python standard library only). No `requirements.txt` needed.

The default database is `~/.snippet_manager/snippets.db` (customizable via `--db`).

## Usage

Run with `python -m src.main [options]`.

bash
# Show help
python -m src.main --help

# List all snippets
python -m src.main list

# Add a new snippet (code via stdin)
python -m src.main add --name hello --lang python
# Then paste code:
# print('Hello World')
#
# # Multiline support

# Search snippets
python -m src.main search hello

# Delete a snippet
python -m src.main delete hello

# Custom DB path
python -m src.main --db ./my_snippets.db list
## Features

- **Add**: Store snippets with unique name, language, and code (multiline via stdin).
- **List**: Display all snippets with ID, name, lang, created date, and full code.
- **Search**: Fuzzy matching (partial) on name, language, or code content.
- **Delete**: Remove snippet by name.
- Local SQLite storage with auto-initialization and directory creation.
- Timestamps and unique constraints for data integrity.

## Dependencies

- Python standard library: `argparse`, `sqlite3`, `os`, `sys`.

## Tests

No tests implemented.

## License

MIT