import argparse
import collections
import json
from pathlib import Path

from mm_context_asr.io import read_jsonl
from mm_context_asr.schema import validate_rows


EXPECTED = {
    "mm_contextasr": 1250,
    "kespeech": 19212,
    "cv_yue": 3525,
    "alimeeting": 2850,
}
FORBIDDEN = ("oss://", "/primus_", "/workspace/", "OSS_ACCESS_KEY", "Signature=")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    report = {}
    for name, expected in EXPECTED.items():
        path = args.root / "data" / name / "test.jsonl"
        rows = list(read_jsonl(path))
        assert validate_rows(iter(rows)) == expected
        assert all(row["dataset"] == name for row in rows)
        report[name] = len(rows)
        if name == "mm_contextasr":
            assert collections.Counter(row["scenario"] for row in rows) == {
                "Irrelevant": 250,
                "Implicit": 250,
                "Explicit": 250,
                "Correction": 250,
                "Repeated Error": 250,
            }
            assert len({row["group_id"] for row in rows}) == 250
    for path in args.root.rglob("*"):
        if path.is_file() and path.suffix not in {".wav", ".flac", ".mp3"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in FORBIDDEN:
                assert token not in text, f"{path}: forbidden token {token}"
    print(json.dumps({"valid": True, "splits": report}, indent=2))


if __name__ == "__main__":
    main()
