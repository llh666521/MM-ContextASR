<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Pipeline](#1-data-pipeline) · [Training](#2-context-training) ·
[Benchmark](#3-mm-contextasr-bench) ·
[Dataset](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench) ·
[Evaluation](#evaluation)

</div>

MM-ContextASR studies how **speech and text history** can jointly improve
LLM-based ASR while reducing error propagation from imperfect transcripts.

## 1. Data Pipeline

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="Scenario-controlled multimodal data construction pipeline">
</p>

- **Entity-driven:** construct long-tail entity and plausible confusion pairs.
- **Scenario-controlled:** generate five types of dialogue history.
- **Multimodal:** synthesize, validate, and align speech-text examples.

## 2. Context Training

<p align="center">
  <img src="assets/training.svg" width="76%" alt="Multimodal context training scheme">
</p>

- **Dialogue order:** interleave historical user inputs and assistant replies.
- **Flexible context:** support No Context, Text-only, Speech-only, and Speech+Text.
- **Current-turn objective:** compute loss only on the current transcript.

| Setting | Historical speech | Historical transcript | Assistant text |
| --- | :---: | :---: | :---: |
| **No Context** | ✗ | ✗ | ✗ |
| **Text-only** | ✗ | ✓ | ✓ |
| **Speech-only** | ✓ | ✗ | ✓ |
| **Speech+Text** | ✓ | ✓ | ✓ |

## 3. MM-ContextASR Bench

- **1,250 examples:** 250 aligned groups with 1,439 released WAV files.
- **Five scenarios:** Irrelevant, Implicit, Explicit, Correction, and Repeated Error.
- **Paired evaluation:** fix current speech and entity while varying only history.

<p align="center">
  <img src="assets/length_distribution.png" width="82%" alt="MM-ContextASR text-length distributions">
</p>

The full benchmark metadata and audio are hosted on
[Hugging Face](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench).

## External Evaluation

The paper also constructs contextual evaluation protocols on three existing
datasets. These are **not part of MM-ContextASR Bench**; we release JSONL
interfaces with context and source audio IDs, but do not redistribute audio.

| Dataset | Rows | Evaluation |
| --- | ---: | --- |
| KeSpeech | 19,212 | multi-accent Mandarin; CER, SER, Recall |
| CV-Yue | 3,525 | Cantonese; t2s CER, SER, Recall |
| AliMeeting Far | 2,850 | target-speaker CER and SER |

## Usage

```python
from datasets import load_dataset

repo = "lilonghao/MM-ContextASR-Bench"
bench = load_dataset(repo, "mm_contextasr", split="test")
```

Available configurations: `mm_contextasr`, `kespeech`, `cv_yue`, and
`alimeeting`.

## Evaluation

```bash
python evaluate.py --references test.jsonl --predictions predictions.jsonl
```

Use `--normalizer zh_t2s` for CV-Yue. Report checkpoint identity, missing
predictions, and request errors with each result.

## License

Code is released under Apache-2.0. Dataset-specific terms are listed on
Hugging Face; upstream licenses apply to external datasets.

## Citation

The paper link and BibTeX entry will be added when available.
