import argparse
import json

from .io import read_jsonl, write_jsonl
from .metrics import score_rows
from .normalize import NORMALIZERS
from .render import render_record
from .schema import validate_rows


def main():
    parser = argparse.ArgumentParser(prog="mm-context-asr")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("input")
    render = commands.add_parser("render")
    render.add_argument("--input", required=True)
    render.add_argument("--mode", required=True)
    render.add_argument("--output", required=True)
    score = commands.add_parser("score")
    score.add_argument("--references", required=True)
    score.add_argument("--predictions", required=True)
    score.add_argument("--normalizer", choices=NORMALIZERS, default="zh")
    score.add_argument("--metrics", nargs="*", default=["cer", "ser", "entity_recall"])
    args = parser.parse_args()

    if args.command == "validate":
        print(json.dumps({"examples": validate_rows(read_jsonl(args.input)), "valid": True}))
    elif args.command == "render":
        write_jsonl(args.output, (render_record(row, args.mode) for row in read_jsonl(args.input)))
    else:
        refs = list(read_jsonl(args.references))
        predictions = {row["id"]: row["prediction"] for row in read_jsonl(args.predictions)}
        result = score_rows(refs, predictions, NORMALIZERS[args.normalizer])
        print(json.dumps({key: value for key, value in result.items() if key in set(args.metrics) | {"examples", "missing_predictions", "entity_examples"}}, indent=2))


if __name__ == "__main__":
    main()
