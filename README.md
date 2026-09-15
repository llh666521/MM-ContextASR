# MM-ContextASR

Official evaluation toolkit for **Multimodal Conversational Context for
LLM-Based ASR: Data Construction, Training, and Benchmark**.

MM-ContextASR studies how an ASR system uses preceding speech and text when
recognizing the current utterance. It provides one interface for four input
settings and four evaluation tracks:

| Input setting | Historical speech | Historical text |
| --- | :---: | :---: |
| No Context |  |  |
| Text-only |  | yes |
| Speech-only | yes |  |
| Speech+Text | yes | yes |

| Track | Task | Evaluation split | Metrics |
| --- | --- | ---: | --- |
| MM-ContextASR Bench | contextual entity ASR | 1,250 examples / 250 aligned groups | entity Recall |
| KeSpeech | multi-accent Mandarin ASR | 19,212 utterances | CER, SER, entity Recall |
| CV-Yue | Cantonese ASR | 3,525 utterances | CER, SER, entity Recall |
| AliMeeting Far-Far v4 | target-speaker ASR | 2,850 overlap segments | target-only CER, SER |

## Highlights

- **Controlled histories.** MM-ContextASR fixes the current speech, reference,
  and target entity while varying five history scenarios.
- **Multimodal inputs.** A canonical record can be rendered as No Context,
  Text-only, Speech-only, or Speech+Text without changing the target turn.
- **Beyond entity correction.** The external-data recipes cover accent,
  dialect, and target-speaker recognition.
- **Reproducible scoring.** Metrics, normalization, missing-output checks, and
  schema validation are included.

## Installation

```bash
git clone https://github.com/llh666521/MM-ContextASR.git
cd MM-ContextASR
pip install -e .
```

The core evaluator uses only the Python standard library.

## Data

The metadata-only benchmark release is hosted separately on Hugging Face:

```python
from datasets import load_dataset

bench = load_dataset("lilonghao/MM-ContextASR-Bench", "mm_contextasr", split="test")
kespeech = load_dataset("lilonghao/MM-ContextASR-Bench", "kespeech", split="test")
cv_yue = load_dataset("lilonghao/MM-ContextASR-Bench", "cv_yue", split="test")
alimeeting = load_dataset("lilonghao/MM-ContextASR-Bench", "alimeeting", split="test")
```

Audio is not mirrored. Each row stores stable source audio identifiers and
enough context to reconstruct the evaluated input. Follow the source dataset's
access terms to resolve identifiers to local audio.

The release includes the 19,212-row KeSpeech evaluation JSONL with source audio
identifiers but no KeSpeech audio. Obtain the corpus from its official source
under the original license. The same manifest can also be regenerated locally:

```bash
python recipes/kespeech/prepare_eval.py \
  --kespeech-root /path/to/KeSpeech \
  --output data/kespeech/test.jsonl
```

## Quick evaluation

Predictions use one JSON object per line:

```json
{"id": "example-id", "prediction": "recognized text"}
```

```bash
mm-context-asr validate path/to/test.jsonl
mm-context-asr score \
  --references path/to/test.jsonl \
  --predictions predictions.jsonl \
  --metrics cer ser entity_recall \
  --normalizer zh
```

For CV-Yue, use `--normalizer zh_t2s`. AliMeeting references are target-speaker
words only; do not score the interfering speakers.

## Input construction

Canonical records retain dialogue order, historical transcript, historical
audio ID, assistant response when present, current audio ID, and current-turn
reference. Render model-facing requests with:

```bash
mm-context-asr render \
  --input canonical.jsonl \
  --mode speech_text \
  --output requests.jsonl
```

Reference text, entities, and scenario labels are never inserted into the
model prompt. See [docs/data.md](docs/data.md) for the schema and
[docs/evaluation.md](docs/evaluation.md) for reporting requirements.

## Repository layout

```text
MM-ContextASR/
├── mm_context_asr/        # schema, rendering, normalization, metrics
├── recipes/               # source-specific metadata preparation
├── scripts/               # command-line utilities
├── docs/                  # protocol and data documentation
├── tests/                 # unit tests and leakage checks
└── results/               # versioned benchmark tables
```

## Reproducibility rules

1. Keep the evaluation IDs and target audio fixed across all four input modes.
2. Preserve historical user, assistant, and current-user order.
3. Report the model checkpoint and adapter identity for every result.
4. Report missing predictions and request errors separately.
5. Do not mix released Base, task-specific SFT, or merged SFT checkpoints.

## License

Code is released under Apache-2.0. Dataset licenses are separate. Common Voice
derived metadata is CC0-1.0; AliMeeting derivatives follow CC BY-SA 4.0. The
KeSpeech config remains subject to the original non-commercial,
no-distribution license. The MM-ContextASR Bench license will be stated in its
final approved dataset card.

## Citation

A BibTeX entry will be added when the paper identifier is available.
