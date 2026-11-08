
from pathlib import Path
import re


def read_cobol_file(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="replace"
    )


def analyze_file(file_path):
    code = read_cobol_file(file_path)

    go_to_matches = re.findall(
        r"\bGO\s+TO\b",
        code,
        re.IGNORECASE
    )

    alter_matches = re.findall(
        r"\bALTER\b",
        code,
        re.IGNORECASE
    )

    return {
        "go_to": len(go_to_matches),
        "alter": len(alter_matches)
    }
