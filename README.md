<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR: Data Construction, Training, and Benchmark

**An LLM-based ASR framework that brings historical user speech, transcripts,
and assistant responses together in dialogue order for current-turn recognition.**

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Dataset](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench) ·
[Method](#method-and-evaluation-design) ·
[Benchmark](#mm-contextasr-bench) ·
[Quick Start](#quick-start) ·
[Evaluation](#evaluation) ·
[Citation](#citation)

</div>

<p align="center">
  <img src="assets/overview.png" width="100%" alt="MM-ContextASR overview">
</p>

<table align="center">
  <tr>
    <td align="center"><strong>872,929</strong><br><sub>constructed training examples</sub></td>
    <td align="center"><strong>174,587</strong><br><sub>entity-confusion anchors</sub></td>
    <td align="center"><strong>4</strong><br><sub>context settings</sub></td>
    <td align="center"><strong>5</strong><br><sub>controlled scenarios</sub></td>
    <td align="center"><strong>3</strong><br><sub>external evaluation tasks</sub></td>
  </tr>
</table>

## News

- **2026-09-15:** We released MM-ContextASR Bench with complete metadata and
  1,439 generated WAV files. We also provide paper-specific evaluation
  interfaces for KeSpeech, CV-Yue, and AliMeeting.

## What This Work Provides

- **Scenario-controlled data construction.** The pipeline builds multimodal
  dialogues around entities and confusable alternatives, including relevant,
  irrelevant, and erroneous histories.
- **Flexible multimodal context training.** Historical user speech, ASR
  transcripts, and assistant responses are interleaved in dialogue order, with
  supervision applied only to the current transcript.
- **Controlled benchmark evaluation.** MM-ContextASR Bench isolates contextual
  understanding and entity correction across five matched history scenarios.
- **Evaluation beyond entity correction.** Paper experiments examine whether
  historical speech provides pronunciation cues for accent and dialect ASR and
  identity cues for target-speaker ASR.

## Released Dataset

| Dataset | Examples | Audio | Context | Primary metric |
| --- | ---: | --- | --- | --- |
| **MM-ContextASR Bench** | **1,250** | **1,439 WAV files** | five controlled dialogue scenarios | entity Recall |

**MM-ContextASR Bench is the dataset released by this project.** Its 250 aligned
groups contain 1,250 examples, with 250 examples for each history scenario.
Current audio and historical audio are included under `audio/current/` and
`audio/history/`.

## Paper Evaluation Interfaces

KeSpeech, CV-Yue, and AliMeeting are **not components or subsets of
MM-ContextASR Bench**. For the experiments in our paper, we construct contextual
evaluation protocols on their official splits and provide the resulting JSONL
as reproducibility and testing interfaces.

| Source dataset | Evaluation rows | Context constructed for the paper | Metrics |
| --- | ---: | --- | --- |
| KeSpeech | 19,212 | same-speaker utterance from the same corpus split | CER, SER, entity Recall |
| CV-Yue | 3,525 | same-speaker utterance from the same corpus split | t2s-normalized CER, SER, entity Recall |
| AliMeeting Far-Far v4 | 2,850 | non-overlapping same-speaker enrollment speech | target-only CER, SER |

These interfaces retain context, audio IDs, and task-specific metadata without
redistributing source audio. Resolve the released IDs against the original
datasets under their upstream licenses.

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

## Method and Evaluation Design

### Multimodal context representations

| Setting | Historical speech | Historical transcript | Assistant text |
| --- | :---: | :---: | :---: |
| **No Context** |  |  |  |
| **Text-only** |  | Yes | Yes |
| **Speech-only** | Yes |  | Yes |
| **Speech+Text** | Yes | Yes | Yes |

Current-turn references, entity labels, and scenario labels are evaluation-only
and must never be inserted into model prompts.

## MM-ContextASR Bench

The released benchmark evaluates contextual understanding and entity correction
while holding the current speech, reference transcript, and target entity fixed.
Only the dialogue history changes within each aligned group.

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
