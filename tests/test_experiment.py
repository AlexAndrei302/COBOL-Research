
from pathlib import Path

from run_experiment import (
    calculate_density,
    analyze_selected_file
)


def test_density_calculation():
    assert calculate_density(5, 250) == 20.0


def test_density_with_zero_warnings():
    assert calculate_density(0, 250) == 0.0


def test_density_with_zero_loc():
    assert calculate_density(5, 0) is None


def test_analyze_realistic_sample(tmp_path):
    file_path = tmp_path / "example.cbl"

    file_path.write_text(
        "       IDENTIFICATION DIVISION.\n"
        "       PROGRAM-ID. EXAMPLE.\n"
        "       PROCEDURE DIVISION.\n"
        "           GO TO END-PROGRAM.\n"
        "       END-PROGRAM.\n"
        "           STOP RUN.\n",
        encoding="utf-8"
    )

    result = analyze_selected_file(file_path)

    assert result["status"] == "ok"
    assert result["go_to"] == 1
    assert result["alter"] == 0
    assert result["total_warnings"] == 1
    assert result["analyzed_code_lines"] == 6
    assert result["warning_density"] == 166.67


def test_missing_file(tmp_path):
    missing_file = tmp_path / "missing.cbl"

    result = analyze_selected_file(missing_file)

    assert result["status"] == "error"
    assert result["error"] != ""
    assert result["total_warnings"] == ""
