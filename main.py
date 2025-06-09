import argparse
from scripts.file_indexer import (
    scan_folder,
    answer_question_human_like,
    open_file_in_explorer,
    organize_folder,
    backup_and_rename,
)


def main():
    parser = argparse.ArgumentParser(description="Danus CLI")
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("scan", help="Index a folder")
    s.add_argument("path")

    a = sub.add_parser("ask", help="Ask a question")
    a.add_argument("question")

    o = sub.add_parser("open", help="Open a file location")
    o.add_argument("path")

    org = sub.add_parser("organize", help="Organize folder by meaning")
    org.add_argument("path")

    b = sub.add_parser("backup", help="Backup and rename a file")
    b.add_argument("file")

    args = parser.parse_args()

    if args.cmd == "scan":
        added = scan_folder(args.path)
        print(f"Indexed {added} files")
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
