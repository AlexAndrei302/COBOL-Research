
from analyzer import read_cobol_file


def main():
    code = read_cobol_file("samples/example.cbl")
    print(code)


if __name__ == "__main__":
    main()
