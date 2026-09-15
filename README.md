<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Pipeline](#1-scenario-controlled-data-construction) · [Training](#2-multimodal-context-training) ·
[Benchmark](#3-mm-contextasr-bench) ·
[Download](#download) ·
[Evaluation](#evaluation)

</div>

MM-ContextASR is a framework for studying how spoken and textual dialogue
history can support current-turn recognition in LLM-based ASR. It comprises
scenario-controlled data construction, multimodal context training, and a
controlled benchmark for contextual understanding and entity correction.

## 1. Scenario-Controlled Data Construction

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="Scenario-controlled multimodal data construction pipeline">
</p>

1. **Entity Pool:** select proper names and long-tail terms across multiple domains.
2. **Confusion Pair Construction:** retrieve phonetic neighbors and select plausible ASR confusions.
3. **Dialogue Generation:** construct five controlled histories around each entity-confusion pair.
4. **Speech Synthesis and Validation:** synthesize user speech and filter low-quality audio with ASR-based checks.
5. **Multimodal Training Data:** package accepted dialogues into aligned Text-only, Speech-only, and Speech+Text examples.

## 2. Multimodal Context Training

<p align="center">
  <img src="assets/training.svg" width="76%" alt="Multimodal context training scheme">
</p>

- **Context representation:** combine historical speech, its ASR transcript, and the assistant response; all context-enabled settings retain assistant responses.
- **Input organization:** interleave historical user and assistant turns in dialogue order, followed by the current speech.
- **Supervision:** use dialogue history only as conditioning information and compute the training loss on the current transcript.

| Setting | Historical speech | Historical transcript | Assistant text |
| --- | :---: | :---: | :---: |
| **No Context** | ✗ | ✗ | ✗ |
| **Text-only** | ✗ | ✓ | ✓ |
| **Speech-only** | ✓ | ✗ | ✓ |
| **Speech+Text** | ✓ | ✓ | ✓ |

## 3. MM-ContextASR Bench

- **Composition:** 250 manually selected target entities and 1,250 examples, with 250 examples per scenario.
- **Scenarios:** Irrelevant, Implicit, Explicit, Correction, and Repeated Error.
- **Paired protocol:** hold the current speech, reference, and target entity fixed while varying only dialogue history.
- **Split integrity:** hold out evaluation entity-confusion pairs and their dialogues from training.
- **Metric:** report entity recall for each scenario and its macro-average as Overall.

<p align="center">
  <img src="assets/length_distribution.png" width="76%" alt="MM-ContextASR text-length distributions">
</p>

## Download

Download the complete MM-ContextASR Bench release, including metadata and
1,439 WAV files, from [Hugging Face](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench):

```bash
git lfs install
git clone https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench
```

Load the benchmark directly with Hugging Face Datasets:

```python
from datasets import load_dataset

bench = load_dataset(
    "lilonghao/MM-ContextASR-Bench",
    "mm_contextasr",
    split="test",
)
```

## External Evaluation

The paper also constructs contextual evaluation protocols on three existing
datasets. These are **not part of MM-ContextASR Bench**; we release JSONL
interfaces with context and source audio IDs, but do not redistribute audio.

| Dataset | Rows | Evaluation |
| --- | ---: | --- |
| KeSpeech | 19,212 | multi-accent Mandarin; CER, SER, Recall |
| CV-Yue | 3,525 | Cantonese; t2s CER, SER, Recall |
| AliMeeting Far | 2,850 | target-speaker CER and SER |

The `kespeech`, `cv_yue`, and `alimeeting` configurations expose the external
evaluation interfaces described above.

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
