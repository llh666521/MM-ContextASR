from mm_context_asr.metrics import edit_distance, score_rows


def test_edit_distance():
    assert edit_distance("abc", "adc") == 1
    assert edit_distance("abc", "") == 3


def test_score_rows():
    refs = [{"id": "1", "current_transcript": "甲乙", "entity": "乙"}]
    result = score_rows(refs, {"1": "甲乙"})
    assert result["cer"] == 0
    assert result["ser"] == 0
    assert result["entity_recall"] == 1


def test_multiple_entities_use_micro_recall():
    refs = [{
        "id": "1",
        "current_transcript": "甲乙丙",
        "entities": [{"text": "甲"}, {"text": "丙"}],
    }]
    result = score_rows(refs, {"1": "甲乙"})
    assert result["entity_recall"] == 0.5
    assert result["entity_examples"] == 2
