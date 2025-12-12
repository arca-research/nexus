from ..src.state import Checksums

from pathlib import Path

def test_checksums_insert_and_skip(tmp_path: Path):
    db_path = tmp_path / "checksums.sqlite"
    checksums = Checksums(db_path)

    docs = [
        "Hello World",
        "Winter Weather",
        "To be or not to be"
    ]

    test_docs = [
        "Hello World", # duplicate
        "This text should not be recorded"
    ]

    # insert initial docs
    for d in docs:
        cs = checksums.compute(d)
        assert not checksums.has(cs)
        checksums.add(cs)
        assert checksums.has(cs)

    # second pass: one duplicate, one new
    cs_dup = checksums.compute(test_docs[0])
    assert checksums.has(cs_dup)

    cs_new = checksums.compute(test_docs[1])
    assert not checksums.has(cs_new)
    checksums.add(cs_new)
    assert checksums.has(cs_new)
