
import pytest

from analyzer import (
    analyze_file,
    extract_code_lines,
    read_cobol_file
)


def run_analyzer(tmp_path, text, source_format="fixed"):
    path = tmp_path / "example.cbl"
    path.write_text(text, encoding="utf-8")

    return analyze_file(
        path, source_format=source_format
    )


def test_detect_go_to(tmp_path):
    result = run_analyzer(
        tmp_path, "       GO TO FINISH.\n"
    )
    assert result["go_to"] == 1


def test_detect_alter(tmp_path):
    result = run_analyzer(
        tmp_path,
        "       ALTER ROUTE TO PROCEED TO FINISH.\n"
    )
    assert result["alter"] == 1


def test_case_insensitive(tmp_path):
    result = run_analyzer(
        tmp_path, "       go to FINISH.\n"
    )
    assert result["go_to"] == 1


def test_ignore_fixed_comment(tmp_path):
    result = run_analyzer(
        tmp_path, "      * GO TO FINISH.\n"
    )
    assert result == {"go_to": 0, "alter": 0}


def test_ignore_double_quoted_literal(tmp_path):
    result = run_analyzer(
        tmp_path, '       DISPLAY "GO TO FINISH".\n'
    )
    assert result["go_to"] == 0


def test_ignore_single_quoted_literal(tmp_path):
    result = run_analyzer(
        tmp_path, "       DISPLAY 'ALTER ROUTE'.\n"
    )
    assert result["alter"] == 0


def test_ignore_inline_comment(tmp_path):
    result = run_analyzer(
        tmp_path,
        "       DISPLAY 'hello'. *> GO TO FINISH\n"
    )
    assert result["go_to"] == 0


def test_ignore_escaped_quotes(tmp_path):
    result = run_analyzer(
        tmp_path,
        '       DISPLAY "it says ""GO TO"" today".\n'
    )
    assert result["go_to"] == 0


def test_free_format(tmp_path):
    result = run_analyzer(
        tmp_path,
        "GO TO FINISH. *> ALTER ROUTE\n",
        source_format="free"
    )
    assert result == {"go_to": 1, "alter": 0}


def test_fixed_continuation_rejected(tmp_path):
    with pytest.raises(ValueError, match="continuation"):
        run_analyzer(
            tmp_path, "      - CONTINUED\n"
        )


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_cobol_file(
            tmp_path / "missing.cbl"
        )


def test_invalid_source_format():
    with pytest.raises(ValueError, match="source_format"):
        extract_code_lines("", "unknown")
