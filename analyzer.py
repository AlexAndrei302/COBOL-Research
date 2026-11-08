
from pathlib import Path
import re


GO_TO_PATTERN = re.compile(
    r"\bGO\s+TO\b", re.IGNORECASE
)
ALTER_PATTERN = re.compile(
    r"\bALTER\b", re.IGNORECASE
)


def read_cobol_file(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="replace"
    )


def mask_literals_and_inline_comments(text):
    """Hide literals and inline comments from detection."""
    result = []
    quote = None
    i = 0

    while i < len(text):
        char = text[i]

        if quote is not None:
            if char == quote:
                if i + 1 < len(text) and text[i + 1] == quote:
                    result.extend("  ")
                    i += 2
                    continue

                quote = None

            result.append(" ")
            i += 1
            continue

        if text[i:i + 2] == "*>":
            result.extend(" " * (len(text) - i))
            break

        if char in ("'", '"'):
            quote = char
            result.append(" ")
        else:
            result.append(char)

        i += 1

    return "".join(result)


def extract_code_lines(source, source_format="fixed"):
    if source_format not in ("fixed", "free"):
        raise ValueError(
            "source_format must be 'fixed' or 'free'"
        )

    code_lines = []

    for line_no, line in enumerate(
        source.splitlines(), start=1
    ):
        if source_format == "fixed":
            if len(line) < 7:
                continue

            indicator = line[6]

            if indicator in ("*", "/", "D", "d"):
                continue

            if indicator == "-":
                raise ValueError(
                    "Fixed-format continuation not "
                    f"supported at line {line_no}"
                )

            if indicator not in (" ", "0"):
                raise ValueError(
                    "Unexpected fixed-format indicator "
                    f"at line {line_no}: {indicator!r}"
                )

            code = line[7:72]
        else:
            if line.lstrip().startswith("*>"):
                continue

            code = line

        code_lines.append(
            mask_literals_and_inline_comments(code)
        )

    return code_lines


def analyze_file(file_path, source_format="fixed"):
    source = read_cobol_file(file_path)

    lines = extract_code_lines(
        source, source_format=source_format
    )

    return {
        "go_to": sum(
            len(GO_TO_PATTERN.findall(line))
            for line in lines
        ),
        "alter": sum(
            len(ALTER_PATTERN.findall(line))
            for line in lines
        )
    }
