
from analyzer import analyze_file


def main():
    file_path = "samples/example.cbl"

    results = analyze_file(file_path)

    print("COBOL Static Analysis")
    print("---------------------")
    print("File:", file_path)
    print("GO TO:", results["go_to"])
    print("ALTER:", results["alter"])


if __name__ == "__main__":
    main()
