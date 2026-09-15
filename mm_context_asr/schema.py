REQUIRED_FIELDS = {
    "id",
    "dataset",
    "split",
    "task",
    "language",
    "current_audio_id",
    "current_transcript",
    "history",
    "source",
}


def validate_record(record):
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"{record.get('id', '<unknown>')}: missing {sorted(missing)}")
    if not isinstance(record["history"], list):
        raise ValueError(f"{record['id']}: history must be a list")
    if not record["current_audio_id"]:
        raise ValueError(f"{record['id']}: current_audio_id is empty")
    if not isinstance(record["current_transcript"], str):
        raise ValueError(f"{record['id']}: current_transcript must be text")
    for turn in record["history"]:
        if turn.get("role") not in {"user", "assistant"}:
            raise ValueError(f"{record['id']}: invalid history role")
        if not ({"text", "audio_id"} & turn.keys()):
            raise ValueError(f"{record['id']}: empty history turn")


def validate_rows(rows):
    seen = set()
    count = 0
    for record in rows:
        validate_record(record)
        if record["id"] in seen:
            raise ValueError(f"duplicate id: {record['id']}")
        seen.add(record["id"])
        count += 1
    return count
