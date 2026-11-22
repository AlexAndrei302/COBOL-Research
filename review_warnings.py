
from pathlib import Path
import csv

from analyzer import (
    read_cobol_file,
    mask_literals_and_inline_comments,
    GO_TO_PATTERN,
    ALTER_PATTERN,
)

RESULTS_FILE = Path("results/experiment_results.csv")
VALIDATION_FILE = Path("results/validation.csv")
ZERO_REVIEW_FILE = Path("results/zero_review.csv")


def find_candidates(file_path, source_format="fixed"):
    source = read_cobol_file(file_path)
    candidates = []

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
                    f"Continuation at line {line_no}"
                )

            if indicator not in (" ", "0"):
                raise ValueError(
                    f"Unexpected indicator at line {line_no}"
                )

            code = line[7:72]

        elif source_format == "free":
            if line.lstrip().startswith("*>"):
                continue

            code = line

        else:
            raise ValueError(
                "Unknown COBOL source format"
            )

        clean = mask_literals_and_inline_comments(code)

        for name, pattern in [
            ("GO TO", GO_TO_PATTERN),
            ("ALTER", ALTER_PATTERN),
        ]:
            for match in pattern.finditer(clean):
                candidates.append({
                    "file_path": Path(file_path).as_posix(),
                    "source_format": source_format,
                    "line_number": line_no,
                    "rule": name,
                    "source_line": line.strip(),
                    "manual_verdict": "",
                    "notes": "",
                })

    return candidates


def read_experiment():
    if not RESULTS_FILE.is_file():
        raise FileNotFoundError(RESULTS_FILE)

    with RESULTS_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def save_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    experiment = read_experiment()

    candidates = []
    zero_files = []

    for row in experiment:
        if row["status"] != "ok":
            continue

        file_path = row["file_path"]
        source_format = row["source_format"]

        detected = find_candidates(
            file_path, source_format
        )

        candidates.extend(detected)

        if int(row["total_warnings"]) == 0:
            zero_files.append({
                "file_path": file_path,
                "source_format": source_format,
                "format_verification": row.get(
                    "format_verification", ""
                ),
                "manual_format": "",
                "manual_go_to": "",
                "manual_alter": "",
                "manual_verdict": "",
                "notes": "",
            })

    validation_fields = [
        "file_path",
        "source_format",
        "line_number",
        "rule",
        "source_line",
        "manual_verdict",
        "notes",
    ]

    zero_fields = [
        "file_path",
        "source_format",
        "format_verification",
        "manual_format",
        "manual_go_to",
        "manual_alter",
        "manual_verdict",
        "notes",
    ]

    save_csv(
        VALIDATION_FILE,
        validation_fields,
        candidates
    )

    save_csv(
        ZERO_REVIEW_FILE,
        zero_fields,
        zero_files
    )

    print("Manual Validation Preparation")
    print("-----------------------------")
    print(f"Warning candidates: {len(candidates)}")
    print(f"Files with zero warnings: {len(zero_files)}")
    print(f"Warning review: {VALIDATION_FILE}")
    print(f"Zero review: {ZERO_REVIEW_FILE}")
    print()
    print("Review the generated CSV files manually.")
    print("Do not treat empty verdicts as validated.")


if __name__ == "__main__":
    main()
