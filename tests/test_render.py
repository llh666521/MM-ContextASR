from mm_context_asr.render import render_record


ROW = {
    "id": "x",
    "dataset": "demo",
    "task": "asr",
    "current_audio_id": "cur.wav",
    "history": [
        {"role": "user", "audio_id": "hist.wav", "text": "hello"},
        {"role": "assistant", "text": "world"},
    ],
}


def test_modes_do_not_leak_text_into_speech_only():
    speech = render_record(ROW, "speech_only")
    assert speech["history"][0] == {"role": "user", "audio_id": "hist.wav"}
    assert speech["history"][1] == {"role": "assistant", "text": "world"}


def test_no_context_is_empty():
    assert render_record(ROW, "no_context")["history"] == []
