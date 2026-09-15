<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR

**A controlled benchmark and evaluation suite for understanding how dialogue
history improves entity, accent, dialect, and target-speaker recognition.**

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=social)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Audio](https://img.shields.io/badge/Audio-1%2C439%20WAV-E7645A)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench/tree/main/audio)
[![License](https://img.shields.io/badge/Code-Apache--2.0-29966F)](LICENSE)

[Dataset](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench) ·
[Benchmark](#benchmark-design) ·
[Quick Start](#quick-start) ·
[Evaluation](#evaluation) ·
[Citation](#citation)

</div>

<p align="center">
  <img src="assets/overview.png" width="100%" alt="MM-ContextASR overview">
</p>

<table align="center">
  <tr>
    <td align="center"><strong>1,250</strong><br><sub>controlled examples</sub></td>
    <td align="center"><strong>250</strong><br><sub>aligned groups</sub></td>
    <td align="center"><strong>5</strong><br><sub>history scenarios</sub></td>
    <td align="center"><strong>4</strong><br><sub>context settings</sub></td>
    <td align="center"><strong>26,837</strong><br><sub>total eval rows</sub></td>
  </tr>
</table>

## News

- **2026-09-15:** MM-ContextASR Bench is public with complete metadata and
  1,439 generated WAV files. Evaluation JSONL for KeSpeech, CV-Yue, and
  AliMeeting is released alongside it.

## Why MM-ContextASR?

- **Controlled context.** The current speech, transcription, and target entity
  stay fixed while only the preceding dialogue changes.
- **Speech and text are evaluated separately.** Four matched input settings
  expose what comes from semantic history and what comes from acoustic cues.
- **Beyond entity correction.** The same protocol extends to multi-accent
  Mandarin, Cantonese, and far-field target-speaker ASR.

## Data Release

| Track | Test examples | Audio in this release | Context signal | Metrics |
| --- | ---: | --- | --- | --- |
| **MM-ContextASR Bench** | **1,250** | **1,439 WAV files** | controlled dialogue | entity Recall |
| KeSpeech | 19,212 | source IDs | multi-accent same-speaker history | CER, SER, Recall |
| CV-Yue | 3,525 | source IDs | Cantonese same-speaker history | CER, SER, Recall |
| AliMeeting Far-Far v4 | 2,850 | segment IDs + timestamps | target-speaker history | target-only CER, SER |

MM-ContextASR audio is included under `audio/current/` and `audio/history/`.
The three external tracks release complete evaluation JSONL and contextual
metadata without redistributing source audio. Their IDs resolve against the
original datasets under the corresponding upstream licenses.

## Quick Start

```bash
pip install datasets
```

```python
from datasets import load_dataset

repo = "lilonghao/MM-ContextASR-Bench"

mm = load_dataset(repo, "mm_contextasr", split="test")
kespeech = load_dataset(repo, "kespeech", split="test")
cv_yue = load_dataset(repo, "cv_yue", split="test")
alimeeting = load_dataset(repo, "alimeeting", split="test")
```

Download the complete release, including MM-ContextASR audio:

```bash
git lfs install
git clone https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench
```

## Benchmark Design

### Four matched context settings

| Setting | Historical speech | Historical transcript | Assistant text |
| --- | :---: | :---: | :---: |
| **No Context** |  |  |  |
| **Text-only** |  | Yes | Yes |
| **Speech-only** | Yes |  | Yes |
| **Speech+Text** | Yes | Yes | Yes |

Current-turn references, entity labels, and scenario labels are evaluation-only
and must never be inserted into model prompts.

### Five controlled history scenarios

| Scenario | Historical evidence | Capability tested |
| --- | --- | --- |
| **Irrelevant** | unrelated topic | ignore distractors |
| **Implicit** | related topic without the entity | use indirect semantic cues |
| **Explicit** | correct entity appears | use direct contextual evidence |
| **Correction** | assistant corrects a historical ASR error | recover from history errors |
| **Repeated Error** | assistant repeats the historical error | resist error propagation |

<details>
<summary><strong>View the JSONL record format</strong></summary>

```json
{
  "id": "0001_explicit",
  "current_audio": "audio/current/0001.wav",
  "current_transcript": "...",
  "history": [
    {"role": "user", "audio": "audio/history/0001.wav", "text": "..."},
    {"role": "assistant", "text": "..."}
  ],
  "scenario": "Explicit",
  "entity": "..."
}
```

Each row preserves current audio, the reference transcription, ordered dialogue
history, source provenance, and task-specific annotations. No internal storage
URI or machine-specific path is included.

</details>

## Dataset Statistics

The controlled histories contain longer linguistic context than the current
queries, while assistant responses provide the richest text signal.

<p align="center">
  <img src="assets/length_distribution.png" width="100%" alt="MM-ContextASR text-length distributions">
</p>

## Evaluation

Predictions use one JSON object per line:

```json
{"id": "0001_explicit", "prediction": "recognized text"}
```

Run the lightweight scorer included in this repository:

```bash
python evaluate.py \
  --references test.jsonl \
  --predictions predictions.jsonl \
  --normalizer zh
```

Use `--normalizer zh_t2s` for CV-Yue. Report checkpoint identity, missing
predictions, and request errors with every result. AliMeeting references contain
target-speaker words only.

## License

The evaluation script is released under Apache-2.0. Dataset terms are listed
per configuration on Hugging Face. External source licenses continue to apply.

## Citation

The paper link and BibTeX entry will be added when the public identifier is
available. Please star this repository or watch the release page for updates.
