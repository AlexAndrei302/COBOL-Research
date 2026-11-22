
from pathlib import Path
import csv

RESULTS_FILE = Path(
    "results/experiment_results.csv"
)


def main():
    if not RESULTS_FILE.is_file():
        print(f"Missing file: {RESULTS_FILE}")
        return

    with RESULTS_FILE.open(
        "r", encoding="utf-8", newline=""
    ) as file:
        results = list(csv.DictReader(file))

    successful = [
        row for row in results
        if row["status"] == "ok"
    ]

    failed = [
        row for row in results
        if row["status"] != "ok"
    ]

    verified = [
        row for row in successful
        if row.get("format_verification") == "manual"
    ]

    go_to = sum(
        int(row["go_to"]) for row in successful
    )

    alter = sum(
        int(row["alter"]) for row in successful
    )

    print("Experiment Summary")
    print("------------------")
    print(f"Selected files: {len(results)}")
    print(f"Successful runs: {len(successful)}")
    print(f"Failed runs: {len(failed)}")
    print(f"Manually verified formats: {len(verified)}")
    print(f"GO TO occurrences: {go_to}")
    print(f"ALTER occurrences: {alter}")
    print(
        f"Total detected occurrences: {go_to + alter}"
    )

    print("\nFiles with detected occurrences:")

    found = False

    for row in successful:
        if int(row["total_warnings"]) > 0:
            found = True
            print(
                f"{Path(row['file_path']).name}: "
                f"{row['total_warnings']}"
            )

    if not found:
        print("No occurrences detected.")

    print("\nFiles with unverified formats:")

    for row in successful:
        if row.get("format_verification") != "manual":
            print(row["file_path"])

    if failed:
        print("\nFailed files:")
        for row in failed:
            print(
                f"{row['file_path']}: "
                f"{row['error']}"
            )


if __name__ == "__main__":
    main()
