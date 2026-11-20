
from pathlib import Path
import csv
import random

DATA_DIR = Path("data/X-COBOL")
OUTPUT_DIR = Path("results")
OUTPUT_FILE = OUTPUT_DIR / "selected_files.csv"

COBOL_EXTENSIONS = {".cbl", ".cob", ".cobol", ".cpy"}
EXCLUDED_FOLDERS = {
    ".git", ".venv", "venv", "__pycache__",
    "node_modules", ".idea"
}

SAMPLE_SIZE = 15
RANDOM_SEED = 42


def find_cobol_files():
    if not DATA_DIR.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATA_DIR}"
        )

    files = []

    for path in DATA_DIR.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(DATA_DIR)

        if any(
            part.lower() in EXCLUDED_FOLDERS
            for part in relative_path.parts[:-1]
        ):
            continue

        if path.suffix.lower() in COBOL_EXTENSIONS:
            files.append(path)

    return sorted(files, key=lambda p: str(p).lower())


def select_sample(files, sample_size=SAMPLE_SIZE):
    if sample_size < 1:
        raise ValueError("Sample size must be positive")

    rng = random.Random(RANDOM_SEED)
    amount = min(sample_size, len(files))

    selected = rng.sample(files, amount)
    return sorted(selected, key=lambda p: str(p).lower())


def save_sample(files):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "file_path",
            "extension"
        ])

        for path in files:
            writer.writerow([
                path.as_posix(),
                path.suffix.lower()
            ])


def main():
    all_files = find_cobol_files()

    print("X-COBOL Sample Preparation")
    print("--------------------------")
    print(f"COBOL files found: {len(all_files)}")

    if not all_files:
        print("No COBOL source files found.")
        return

    selected = select_sample(all_files)
    save_sample(selected)

    print(f"Selected files: {len(selected)}")
    print(f"Random seed: {RANDOM_SEED}")
    print()

    for path in selected:
        print(path.as_posix())

    print()
    print(f"Sample saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
