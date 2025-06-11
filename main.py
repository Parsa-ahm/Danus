"""Simple command-line interface for Danus."""

import argparse
import os

# ensure local modules are discoverable
os.environ.setdefault("PYTHONPATH", os.getcwd())
os.environ.setdefault("DANUS_SKIP_MODEL", "1")

from scripts.file_indexer import (
    scan_folder,
    answer_question_human_like,
    open_file_in_explorer,
    organize_folder,
    backup_and_rename,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Danus CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    scan_p = sub.add_parser("scan", help="Index a folder")
    scan_p.add_argument("path")

    ask_p = sub.add_parser("ask", help="Ask a question about indexed files")
    ask_p.add_argument("question")

    open_p = sub.add_parser("open", help="Open a file in your OS explorer")
    open_p.add_argument("path")

    org_p = sub.add_parser("organize", help="Organize folder by meaning")
    org_p.add_argument("path")

    backup_p = sub.add_parser("backup", help="Backup and rename a file")
    backup_p.add_argument("file")

    args = parser.parse_args()

    if args.cmd == "scan":
        count = scan_folder(args.path)
        print(f"Indexed {count} files")
    elif args.cmd == "ask":
        result = answer_question_human_like(args.question)
        print(result["summary"])
        for m in result["matches"]:
            print(f"- {m['path']}: {m['preview']}")
    elif args.cmd == "open":
        open_file_in_explorer(args.path)
    elif args.cmd == "organize":
        organize_folder(args.path)
        print("Organization complete")
    elif args.cmd == "backup":
        new_path = backup_and_rename(args.file)
        print(f"Backed up and renamed to {new_path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
