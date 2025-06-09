"""Simple command-line interface for Danus."""

import argparse
import os

# ensure local modules are discoverable
os.environ.setdefault("PYTHONPATH", os.getcwd())
os.environ.setdefault("DANUS_SKIP_MODEL", "1")

from scripts import (
    scan_folder,
    answer_question_human_like,
    open_file_in_explorer,
)


def cmd_scan(args: argparse.Namespace) -> None:
    count = scan_folder(args.path)
    print(f"Indexed {count} file(s)")


def cmd_ask(args: argparse.Namespace) -> None:
    result = answer_question_human_like(args.question)
    print(result["summary"])
    for match in result["matches"]:
        print("-", match["path"])


def cmd_open(args: argparse.Namespace) -> None:
    open_file_in_explorer(args.path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Danus CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="Index a folder")
    p_scan.add_argument("path")
    p_scan.set_defaults(func=cmd_scan)

    p_ask = sub.add_parser("ask", help="Ask a question about indexed files")
    p_ask.add_argument("question")
    p_ask.set_defaults(func=cmd_ask)

    p_open = sub.add_parser("open", help="Open a file in your OS explorer")
    p_open.add_argument("path")
    p_open.set_defaults(func=cmd_open)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
