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


def score_rows(references, predictions, normalize=lambda text: text):
    char_errors = 0
    char_total = 0
    sentence_errors = 0
    entity_hits = 0
    entity_total = 0
    missing = 0
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
        entity_hits += sum(normalize(entity["text"]) in hyp for entity in entities)
    count = len(references)
    return {
        "examples": count,
        "missing_predictions": missing,
        "cer": char_errors / char_total if char_total else None,
        "ser": sentence_errors / count if count else None,
        "entity_recall": entity_hits / entity_total if entity_total else None,
        "entity_examples": entity_total,
    }
