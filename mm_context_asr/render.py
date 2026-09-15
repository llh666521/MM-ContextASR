MODES = {"no_context", "text_only", "speech_only", "speech_text"}


def render_record(record, mode):
    if mode not in MODES:
        raise ValueError(f"unknown context mode: {mode}")
    history = []
    if mode != "no_context":
        for turn in record["history"]:
            item = {"role": turn["role"]}
            if "text" in turn:
                if turn["role"] == "assistant" or mode in {"text_only", "speech_text"}:
                    item["text"] = turn["text"]
            if "audio_id" in turn and mode in {"speech_only", "speech_text"}:
                item["audio_id"] = turn["audio_id"]
            if len(item) > 1:
                history.append(item)
    return {
        "id": record["id"],
        "dataset": record["dataset"],
        "task": record["task"],
        "context_mode": mode,
        "history": history,
        "current_audio_id": record["current_audio_id"],
    }
