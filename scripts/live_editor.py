import difflib
import os
from typing import List, Dict


def suggest_edits(original: str, edited: str) -> List[Dict[str, str]]:
    """Return a list of edit suggestions comparing two strings."""
    diff = difflib.ndiff(original.splitlines(), edited.splitlines())
    suggestions = []
    for line in diff:
        if line.startswith('- '):
            suggestions.append({'type': 'delete', 'text': line[2:]})
        elif line.startswith('+ '):
            suggestions.append({'type': 'add', 'text': line[2:]})
    return suggestions


def apply_edits(path: str, new_text: str, backup: bool = True) -> None:
    """Overwrite a file with new_text and optionally create a backup."""
    if backup and os.path.exists(path):
        os.rename(path, path + '.bak')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
