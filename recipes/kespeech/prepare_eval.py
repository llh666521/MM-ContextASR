import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kespeech-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.parse_args()
    raise SystemExit(
        "The public recipe skeleton is installed, but the frozen pairing index "
        "must be added after its identifier-only release is approved."
    )


if __name__ == "__main__":
    main()
