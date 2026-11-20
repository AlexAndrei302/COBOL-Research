
from pathlib import Path
import csv

DATA_DIR = Path("data/X-COBOL")


def inspect_csv_file(path):
    print(f"\nCSV: {path.as_posix()}")

    try:
        with path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            sample = file.read(4096)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(
                    sample, delimiters=",;\t"
                )
            except csv.Error:
                dialect = csv.excel

            reader = csv.reader(file, dialect)
            header = next(reader, None)

            if header is None:
                print("Empty CSV file")
                return

            print("Columns:")
            for column in header:
                print(f"  - {column}")

            print("First two rows:")
            for _, row in zip(range(2), reader):
                print(row)

    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Could not read CSV: {error}")


def main():
    if not DATA_DIR.is_dir():
        print(f"Missing directory: {DATA_DIR}")
        return

    csv_files = sorted(
        path for path in DATA_DIR.rglob("*.csv")
        if not any(
            part.lower() in {
                "venv", ".venv", ".git", "__pycache__"
            }
            for part in path.relative_to(DATA_DIR).parts[:-1]
        )
    )

    print(f"CSV files found: {len(csv_files)}")

    for path in csv_files:
        inspect_csv_file(path)


if __name__ == "__main__":
    main()
