<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR: Data Construction, Training, and Benchmark

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Pipeline](#1-scenario-controlled-data-construction) ·
[Training](#2-multimodal-context-training) ·
[Benchmark](#3-mm-contextasr-bench) ·
[Dataset](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench) ·
[Evaluation](#evaluation) ·
[Citation](#citation)

</div>

Textual dialogue history provides semantic cues for ASR, but it may propagate
historical recognition errors and cannot fully preserve pronunciation, accent,
or speaker characteristics. We present an LLM-based ASR framework with
**multimodal conversational context**, comprising scenario-controlled data
construction, flexible multimodal context training, and benchmark evaluation.

<table align="center">
  <tr>
    <td align="center"><strong>872,929</strong><br><sub>constructed training examples</sub></td>
    <td align="center"><strong>174,587</strong><br><sub>entity-confusion anchors</sub></td>
    <td align="center"><strong>4</strong><br><sub>context settings</sub></td>
    <td align="center"><strong>1,250</strong><br><sub>benchmark examples</sub></td>
    <td align="center"><strong>3</strong><br><sub>external evaluation protocols</sub></td>
  </tr>
</table>

## News

- **2026-09-15:** We released MM-ContextASR Bench with complete metadata and
  1,439 generated WAV files. We also provide paper-specific testing interfaces
  for the KeSpeech, CV-Yue, and AliMeeting experiments.

## 1. Scenario-Controlled Data Construction

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="Scenario-controlled multimodal data construction pipeline">
</p>

<p align="center"><em>Confusion-pair construction, controlled dialogue generation, speech synthesis and validation, and aligned multimodal training examples.</em></p>

The pipeline constructs conversational ASR data around long-tail entities and
their plausible recognition confusions:

1. **Entity pool:** collect proper names and long-tail terms spanning people,
   places, organizations, products, and technical terminology.
2. **Confusion pairs:** retrieve homophones and near-homophones and select a
   plausible ASR misrecognition for each target entity.
3. **Controlled dialogues:** generate relevant, irrelevant, and erroneous
   histories while keeping the current query fixed.
4. **Speech synthesis and validation:** synthesize historical and current user
   speech, then filter low-quality audio using ASR-based checks.
5. **Aligned multimodal data:** package identical dialogues into Text-only,
   Speech-only, and Speech+Text representations.

The resulting training set contains 872,929 examples across five scenarios from
174,587 entity-confusion anchors.

## 2. Multimodal Context Training

<p align="center">
  <img src="assets/training.svg" width="76%" alt="Multimodal context training scheme">
</p>

<p align="center"><em>Historical user inputs and assistant replies are interleaved in dialogue order; only the current transcript is supervised.</em></p>

Historical user speech, its ASR transcript, and the assistant response are
organized as ordered user-assistant turns before the current speech. This
structure supports different modality combinations and extends naturally to
multiple historical turns without changing the current-turn ASR objective.

| Setting | Historical speech | Historical transcript | Assistant text |
| --- | :---: | :---: | :---: |
| **No Context** | ✗ | ✗ | ✗ |
| **Text-only** | ✗ | ✓ | ✓ |
| **Speech-only** | ✓ | ✗ | ✓ |
| **Speech+Text** | ✓ | ✓ | ✓ |

Historical content is conditioning information only. The loss is computed over
the current reference transcript; current references, entity labels, and
scenario labels are never inserted into model prompts.

## 3. MM-ContextASR Bench

MM-ContextASR Bench evaluates contextual understanding and entity correction
with multimodal dialogue histories. Each aligned group fixes the current speech,
reference transcript, and target entity while changing only the history,
enabling paired comparisons across scenarios and modalities.

| Released dataset | Examples | Audio | Organization | Primary metric |
| --- | ---: | --- | --- | --- |
| **MM-ContextASR Bench** | **1,250** | **1,439 WAV files** | 250 aligned groups × 5 scenarios | entity Recall |

MM-ContextASR Bench is the dataset released by this project. Its current and
historical audio are available under `audio/current/` and `audio/history/` on
[Hugging Face](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench).

### Controlled history scenarios

| Scenario | Historical evidence | Capability tested |
| --- | --- | --- |
| **Irrelevant** | unrelated topic | ignore distractors |
| **Implicit** | related topic without the entity | use indirect semantic cues |
| **Explicit** | correct entity appears | use direct contextual evidence |
| **Correction** | assistant corrects a historical ASR error | recover from history errors |
| **Repeated Error** | assistant repeats the historical error | resist error propagation |

### Dataset statistics

<p align="center">
  <img src="assets/length_distribution.png" width="100%" alt="MM-ContextASR text-length distributions">
</p>

<p align="center"><em>Text lengths in MM-ContextASR Bench, measured in characters after removing whitespace; dashed lines indicate means.</em></p>

<details>
<summary><strong>View the released JSONL format</strong></summary>

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

</details>

## External Evaluation Protocols

KeSpeech, CV-Yue, and AliMeeting are **not components or subsets of
MM-ContextASR Bench**. They are source datasets on which we construct contextual
evaluation protocols for the paper. This repository provides the corresponding
JSONL as reproducibility and testing interfaces, without redistributing their
audio.

| Source dataset | Evaluation rows | Context construction | Metrics |
| --- | ---: | --- | --- |
| KeSpeech | 19,212 | same-speaker utterance from the same corpus split | CER, SER, entity Recall |
| CV-Yue | 3,525 | same-speaker utterance from the same corpus split | t2s-normalized CER, SER, entity Recall |
| AliMeeting Far-Far v4 | 2,850 | non-overlapping same-speaker enrollment speech | target-only CER, SER |

The interfaces retain ordered context, source audio IDs, and task-specific
metadata. Resolve the IDs against each original dataset under its upstream
license.

## Quick Start

```bash
pip install datasets
```

```python
from datasets import load_dataset

repo = "lilonghao/MM-ContextASR-Bench"

# Released benchmark with audio
bench = load_dataset(repo, "mm_contextasr", split="test")

# Paper evaluation interfaces; source audio is not redistributed
kespeech = load_dataset(repo, "kespeech", split="test")
cv_yue = load_dataset(repo, "cv_yue", split="test")
alimeeting = load_dataset(repo, "alimeeting", split="test")
```

Download the complete MM-ContextASR Bench release:

```bash
git lfs install
git clone https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench
```

## Evaluation

Predictions use one JSON object per line:

```json
{"id": "0001_explicit", "prediction": "recognized text"}
```

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
available.
