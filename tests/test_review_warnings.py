
from review_warnings import find_candidates


def test_fixed_format_detection(tmp_path):
    path = tmp_path / "fixed.cbl"

    path.write_text(
        "000100 IDENTIFICATION DIVISION.\n"
        "000200 PROCEDURE DIVISION.\n"
        "000300     GO TO FINISH.\n",
        encoding="utf-8"
    )

    result = find_candidates(path, "fixed")

    assert len(result) == 1
    assert result[0]["rule"] == "GO TO"
    assert result[0]["line_number"] == 3


def test_free_format_detection(tmp_path):
    path = tmp_path / "free.cbl"

    path.write_text(
        "identification division.\n"
        "procedure division.\n"
        "go to finish.\n",
        encoding="utf-8"
    )

    result = find_candidates(path, "free")

    assert len(result) == 1
    assert result[0]["rule"] == "GO TO"
    assert result[0]["line_number"] == 3


def test_free_format_comments(tmp_path):
    path = tmp_path / "comments.cbl"

    path.write_text(
        "*> GO TO FINISH.\n"
        "display 'ALTER'.\n"
        "go to finish.\n",
        encoding="utf-8"
    )

    result = find_candidates(path, "free")

    assert len(result) == 1
    assert result[0]["rule"] == "GO TO"


def test_no_warnings(tmp_path):
    path = tmp_path / "clean.cbl"

    path.write_text(
        "identification division.\n"
        "procedure division.\n"
        "stop run.\n",
        encoding="utf-8"
    )

    result = find_candidates(path, "free")

    assert result == []
