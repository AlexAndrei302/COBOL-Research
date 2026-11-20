
from pathlib import Path

from prepare_sample import select_sample


def test_sample_size():
    files = [
        Path(f"file_{i}.cbl")
        for i in range(30)
    ]

    selected = select_sample(files, 15)

    assert len(selected) == 15


def test_reproducible_selection():
    files = [
        Path(f"file_{i}.cbl")
        for i in range(30)
    ]

    first = select_sample(files, 15)
    second = select_sample(files, 15)

    assert first == second


def test_small_dataset():
    files = [
        Path("one.cbl"),
        Path("two.cbl")
    ]

    selected = select_sample(files, 15)

    assert len(selected) == 2
    assert set(selected) == set(files)


def test_empty_dataset():
    selected = select_sample([], 15)

    assert selected == []


def test_invalid_sample_size():
    try:
        select_sample([Path("one.cbl")], 0)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"
