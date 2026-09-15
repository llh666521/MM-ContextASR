# Evaluation protocol

## Metrics

- **CER:** corpus-level character edit distance divided by reference characters.
- **SER:** fraction of utterances whose normalized prediction differs from the reference.
- **Entity Recall:** fraction of annotated entity mentions present in the prediction.

Remove punctuation and whitespace for Chinese CER. CV-Yue additionally applies
OpenCC `t2s` to both reference and prediction. Report percentages to two decimal
places, sample count, request errors, and missing outputs.

## Context modes

No Context omits every historical turn. Text-only retains historical text.
Speech-only retains historical user speech and any assistant text reply.
Speech+Text retains both historical user modalities and assistant replies.
The current audio and target reference must remain identical across modes.

## Paired reporting

MM-ContextASR examples form 250 groups with five histories each. Use group-aware
confidence intervals or paired tests. A No Context prediction may be decoded
once per current audio and reused across its five histories.
