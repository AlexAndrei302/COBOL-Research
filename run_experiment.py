
from pathlib import Path
import csv

from analyzer import (
    analyze_file,
    read_cobol_file,
    extract_code_lines,
)

INPUT_FILE = Path("results/selected_files.csv")
OUTPUT_FILE = Path("results/experiment_results.csv")

# Formats confirmed manually.
# Other selected files still require verification.
FREE_FORMAT_FILES = {
    "brazilofmux_gnucobol/clinkages.cbl",
}

FIXED_FORMAT_FILES = {
    "gbeine_COBOLUnit/CBU00006.cob",
}


def get_source_format(file_path):
    path = Path(file_path).as_posix()

    for known_path in FREE_FORMAT_FILES:
        if path.endswith(known_path):
            return "free", "manual"

    for known_path in FIXED_FORMAT_FILES:
        if path.endswith(known_path):
            return "fixed", "manual"

    return "fixed", "assumed"


def calculate_density(warnings, loc):
    if loc <= 0:
        return None

    return round(warnings / loc * 1000, 2)


def analyze_selected_file(
    file_path, source_format="fixed"
):
    path = Path(file_path)

    result = {
        "file_path": path.as_posix(),
        "source_format": source_format,
        "format_verification": "not_verified",
        "status": "error",
        "source_lines": "",
        "analyzed_code_lines": "",
        "go_to": "",
        "alter": "",
        "total_warnings": "",
        "warning_density": "",
        "error": "",
    }

    try:
        source = read_cobol_file(path)

        lines = extract_code_lines(
            source, source_format=source_format
        )

        analyzed_loc = sum(
            1 for line in lines if line.strip()
        )

        warnings = analyze_file(
            path, source_format=source_format
        )

        total = warnings["go_to"] + warnings["alter"]
        density = calculate_density(total, analyzed_loc)

        result.update({
            "status": "ok",
            "source_lines": len(source.splitlines()),
            "analyzed_code_lines": analyzed_loc,
            "go_to": warnings["go_to"],
            "alter": warnings["alter"],
            "total_warnings": total,
            "warning_density": (
                density if density is not None else ""
            ),
        })

    except (OSError, UnicodeError, ValueError) as error:
        result["error"] = str(error)

    return result


def read_selected_files():
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(
            f"Missing sample file: {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        if "file_path" not in (reader.fieldnames or []):
            raise ValueError(
                "Missing file_path column"
            )

        return [
            row["file_path"]
            for row in reader
            if row.get("file_path")
        ]


def save_results(results):
    OUTPUT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    fieldnames = [
        "file_path",
        "source_format",
        "format_verification",
        "status",
        "source_lines",
        "analyzed_code_lines",
        "go_to",
        "alter",
        "total_warnings",
        "warning_density",
        "error",
    ]

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(results)


def main():
    selected_files = read_selected_files()
    results = []

    print("X-COBOL Experimental Analysis")
    print("-----------------------------")
    print(f"Selected files: {len(selected_files)}")
    print()

    for file_path in selected_files:
        source_format, verification = get_source_format(
            file_path
        )

        result = analyze_selected_file(
            file_path, source_format
        )

        result["format_verification"] = verification
        results.append(result)

        print(f"File: {Path(file_path).name}")
        print(f"Format: {source_format}")
        print(f"Format verification: {verification}")
        print(f"Status: {result['status']}")

        if result["status"] == "ok":
            print(f"GO TO: {result['go_to']}")
            print(f"ALTER: {result['alter']}")
            print(f"Warnings: {result['total_warnings']}")
            print(
                "Analyzed code lines: "
                f"{result['analyzed_code_lines']}"
            )
            print(
                f"Density: {result['warning_density']}"
            )
        else:
            print(f"Error: {result['error']}")

        print()

    save_results(results)

    successful = sum(
        row["status"] == "ok" for row in results
    )
    failed = len(results) - successful

    verified = sum(
        row["status"] == "ok"
        and row["format_verification"] == "manual"
        for row in results
    )

    print("Experiment Summary")
    print("------------------")
    print(f"Successfully analyzed: {successful}")
    print(f"Failed: {failed}")
    print(f"Manually verified formats: {verified}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
