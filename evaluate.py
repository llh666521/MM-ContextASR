#!/usr/bin/env python3
"""Lightweight CER, SER, and entity-recall scorer for MM-ContextASR."""

import argparse
import json
import re
import unicodedata
from pathlib import Path


PUNCT = re.compile(r"[^\w\u3400-\u9fff]+", re.UNICODE)


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def normalize_zh(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return PUNCT.sub("", text)


def build_normalizer(name):
    if name == "none":
        return lambda text: text
    if name == "zh":
        return normalize_zh
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise SystemExit(
            "zh_t2s requires: pip install opencc-python-reimplemented"
        ) from exc
    converter = OpenCC("t2s")
    return lambda text: normalize_zh(converter.convert(text))


def edit_distance(reference, hypothesis):
    previous = list(range(len(hypothesis) + 1))
    for i, ref_item in enumerate(reference, 1):
        current = [i]
        for j, hyp_item in enumerate(hypothesis, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (ref_item != hyp_item),
                )
            )
        previous = current
    return previous[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--references", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--normalizer", choices=("none", "zh", "zh_t2s"), default="zh")
    args = parser.parse_args()

    references = read_jsonl(args.references)
    predictions = {
        row["id"]: row["prediction"] for row in read_jsonl(args.predictions)
    }
    normalize = build_normalizer(args.normalizer)

    char_errors = char_total = sentence_errors = missing = 0
    entity_hits = entity_total = 0
    for row in references:
        ref = normalize(row["current_transcript"])
        raw_hyp = predictions.get(row["id"])
        if raw_hyp is None:
            missing += 1
            raw_hyp = ""
        hyp = normalize(raw_hyp)
        char_errors += edit_distance(ref, hyp)
        char_total += len(ref)
        sentence_errors += ref != hyp
        entities = row.get("entities")
        if entities is None:
            entities = [{"text": row["entity"]}] if row.get("entity") else []
        entity_total += len(entities)
        entity_hits += sum(normalize(item["text"]) in hyp for item in entities)

    count = len(references)
    result = {
        "examples": count,
        "missing_predictions": missing,
        "cer": char_errors / char_total if char_total else None,
        "ser": sentence_errors / count if count else None,
        "entity_recall": entity_hits / entity_total if entity_total else None,
        "entities": entity_total,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
