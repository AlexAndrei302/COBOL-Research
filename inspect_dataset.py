from pathlib import Path
import csv

DATA_DIR = Path("data/X-COBOL")


def inspect_dataset():
    if not DATA_DIR.exists():
        print("Dataset directory not found.")
        return

    all_files = [
        file for file in DATA_DIR.rglob("*")
        if file.is_file()
    ]

    print("Total files found:", len(all_files))

    csv_files = [
        file for file in all_files
        if file.suffix.lower() == ".csv"
    ]

    print("\nCSV files:")
    for file in csv_files:
        print("-", file.relative_to(DATA_DIR))

    print("\nCOBOL source file examples:")

    cobol_extensions = {".cbl", ".cob", ".cobol", ".cpy"}

    cobol_files = [
        file for file in all_files
        if file.suffix.lower() in cobol_extensions
    ]

    print("Files with known COBOL extensions:",
          len(cobol_files))

    for file in cobol_files[:5]:
        print("-", file.relative_to(DATA_DIR))

    metadata = list(
        DATA_DIR.rglob("cobol_files_data.csv")
    )

    if metadata:
        print("\nMetadata columns:")

        with metadata[0].open(
            encoding="utf-8-sig", newline=""
        ) as f:
            reader = csv.reader(f)
            header = next(reader, [])
            print(header)


if __name__ == "__main__":
    inspect_dataset()
