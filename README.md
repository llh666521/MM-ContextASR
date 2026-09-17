<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Data Pipeline](#data-pipeline) · [Context Training](#context-training) ·
[Benchmark & Evaluation](#benchmark--evaluation) · [Download](#download)

</div>

MM-ContextASR studies how spoken and textual dialogue history can improve
current-turn recognition in LLM-based ASR. The project brings together
scenario-controlled data construction, multimodal context training, and
entity-sensitive evaluation in a single framework.

<p align="center">
  <img src="assets/overview.png" width="100%" alt="MM-ContextASR project overview">
</p>

## Highlights

- **Data Pipeline:** A scenario-controlled pipeline for constructing entity-centric multimodal conversational contexts.
- **Context Training:** A unified training framework supporting text, speech, and joint speech-text dialogue histories.
- **Benchmark & Evaluation:** MM-ContextASR Bench for evaluating contextual ASR across diverse dialogue scenarios, complemented by reproducible protocols for KeSpeech, CV-Yue, and AliMeeting Far.

## Data Pipeline

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="Scenario-controlled multimodal data construction pipeline">
</p>

The pipeline proceeds through five stages:

- **Entity Selection:** Collect proper names and long-tail entities spanning people, places, organizations, products, and technical terms.
- **Confusion Construction:** Construct phonetically grounded ASR confusions from homophones and near-homophones, then select a plausible alternative for each entity.
- **Dialogue Generation:** Generate the current query and its dialogue history under five controlled contextual scenarios.
- **Speech Synthesis:** Synthesize historical and current user queries into speech and verify them through ASR retranscription.
- **Quality Control:** Filter degraded speech and structurally invalid dialogues before packaging the accepted samples into aligned multimodal examples.

## Context Training

<p align="center">
  <img src="assets/training.svg" width="78%" alt="Multimodal context training framework">
</p>

Historical speech, its ASR transcript, and assistant responses are interleaved
in dialogue order before the current speech. Dialogue history is used only as
conditioning information, while the training loss is computed on the current
transcript.

<table>
  <thead>
    <tr>
      <th>Setting</th>
      <th>Historical<br>speech</th>
      <th>Historical<br>transcript</th>
      <th>Assistant<br>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>No Context</strong></td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>
    <tr>
      <td><strong>Text-only</strong></td>
      <td>✗</td>
      <td>✓</td>
      <td>✓</td>
    </tr>
    <tr>
      <td><strong>Speech-only</strong></td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
    </tr>
    <tr>
      <td><strong>Speech+Text</strong></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
    </tr>
  </tbody>
</table>

## Benchmark & Evaluation

**MM-ContextASR Bench** is the benchmark released by this project. It contains
five controlled dialogue scenarios: **Irrelevant**, **Implicit**, **Explicit**,
**Correction**, and **Repeated Error**. Each aligned group keeps the current
speech, reference transcript, and target entity fixed while varying only the
dialogue history. The primary metric is entity recall.

<p align="center">
  <img src="assets/length_distribution.png" width="62%" alt="Text-length distributions in MM-ContextASR Bench">
</p>

The paper additionally reports contextual ASR results on three existing
datasets. These evaluation interfaces are provided for reproduction and are
not part of MM-ContextASR Bench.

| Evaluation protocol | Test set | Metrics |
| --- | --- | --- |
| KeSpeech | 19,212 | CER, SER, entity recall |
| CV-Yue | 3,525 | t2s CER, SER, entity recall |
| AliMeeting Far | 2,850 | target-speaker CER, SER |

## Results

All results are percentages. Bold marks the best value for each metric under
the comparison scope used in the paper, including ties.

### MM-ContextASR Bench

| Model | Training | Context | Irrelevant ↑ | Implicit ↑ | Explicit ↑ | Correction ↑ | Repeated Error ↑ | Overall ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-Omni-Instruct | Base | No Context | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 |
| Qwen3-Omni-Instruct | Base | Text-only | 68.40 | 74.00 | 95.60 | 96.00 | 67.60 | 80.32 |
| Qwen3-Omni-Instruct | Base | Speech-only | 65.60 | 74.40 | 92.40 | 96.40 | 72.00 | 80.16 |
| Qwen3-Omni-Instruct | Base | Speech+Text | 69.60 | 77.60 | 97.60 | 97.60 | 71.60 | 82.80 |
| Qwen3-Omni-Instruct | Context SFT | No Context | **76.80** | 76.80 | 76.80 | 76.80 | 76.80 | 76.80 |
| Qwen3-Omni-Instruct | Context SFT | Text-only | 76.40 | 83.20 | 97.20 | 98.40 | 77.20 | 86.48 |
| Qwen3-Omni-Instruct | Context SFT | Speech-only | 76.40 | 82.40 | 98.40 | 98.40 | **82.80** | 87.68 |
| Qwen3-Omni-Instruct | Context SFT | Speech+Text | 75.60 | **83.60** | **98.80** | **98.80** | 82.40 | **87.84** |
| Step-Audio-2-mini | Base | No Context | 67.20 | 67.20 | 67.20 | 67.20 | 67.20 | 67.20 |
| Step-Audio-2-mini | Base | Text-only | 63.20 | 63.20 | 93.20 | 90.00 | 52.80 | 72.48 |
| Step-Audio-2-mini | Base | Speech-only | 64.80 | 63.20 | 91.60 | 89.20 | 59.20 | 73.60 |
| Step-Audio-2-mini | Base | Speech+Text | 64.40 | 66.40 | 95.60 | 91.20 | 53.20 | 74.16 |
| Step-Audio-2-mini | Context SFT | No Context | **72.80** | 72.80 | 72.80 | 72.80 | 72.80 | 72.80 |
| Step-Audio-2-mini | Context SFT | Text-only | 70.80 | 76.00 | 96.00 | 97.60 | 77.40 | 83.56 |
| Step-Audio-2-mini | Context SFT | Speech-only | **72.80** | 75.60 | **97.20** | **98.40** | 80.80 | 84.96 |
| Step-Audio-2-mini | Context SFT | Speech+Text | 72.00 | **76.80** | 96.80 | **98.40** | **82.00** | **85.20** |

### Accent and Dialect ASR

CV-Yue uses simplified-Chinese normalization.

| Dataset | Training | Context | Recall ↑ | CER ↓ | SER ↓ |
| --- | --- | --- | --- | --- | --- |
| KeSpeech | Base | No Context | 80.16 | 6.60 | 35.58 |
| KeSpeech | Base | Text-only | 78.78 | 6.88 | 36.54 |
| KeSpeech | Base | Speech-only | 78.73 | 6.42 | 36.79 |
| KeSpeech | Base | Speech+Text | 79.13 | 6.30 | 36.10 |
| KeSpeech | Context SFT | No Context | 83.71 | 4.51 | 29.56 |
| KeSpeech | Context SFT | Text-only | 83.90 | 4.40 | 29.14 |
| KeSpeech | Context SFT | Speech-only | **84.93** | 4.19 | 28.39 |
| KeSpeech | Context SFT | Speech+Text | **84.93** | **4.17** | **28.20** |
| CV-Yue | Base | No Context | 85.32 | 4.59 | 30.72 |
| CV-Yue | Base | Text-only | 81.01 | 5.10 | 33.67 |
| CV-Yue | Base | Speech-only | 81.27 | 4.95 | 32.68 |
| CV-Yue | Base | Speech+Text | 83.04 | 4.79 | 32.28 |
| CV-Yue | Context SFT | No Context | **88.10** | 4.89 | 33.08 |
| CV-Yue | Context SFT | Text-only | 85.06 | 4.14 | 28.51 |
| CV-Yue | Context SFT | Speech-only | 87.85 | 3.83 | 26.36 |
| CV-Yue | Context SFT | Speech+Text | 87.85 | **3.74** | **26.33** |

### Target-Speaker ASR

Results on 2,850 overlapping far-field AliMeeting segments.

| Dataset | Training | Context | CER ↓ | SER ↓ |
| --- | --- | --- | --- | --- |
| AliMeeting Far | Base | No Context | 29.70 | 82.74 |
| AliMeeting Far | Base | Text-only | 31.87 | 82.98 |
| AliMeeting Far | Base | Speech-only | 33.26 | 81.30 |
| AliMeeting Far | Base | Speech+Text | 32.23 | 81.40 |
| AliMeeting Far | Context SFT | No Context | 30.25 | 75.61 |
| AliMeeting Far | Context SFT | Text-only | 29.60 | 74.60 |
| AliMeeting Far | Context SFT | Speech-only | **24.59** | 72.18 |
| AliMeeting Far | Context SFT | Speech+Text | 24.80 | **71.96** |

## Download

Download the benchmark metadata and audio from
[Hugging Face](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench):

```bash
git lfs install
git clone https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench
```

Or load a configuration directly with Hugging Face Datasets:

```python
from datasets import load_dataset

bench = load_dataset(
    "lilonghao/MM-ContextASR-Bench",
    "mm_contextasr",
    split="test",
)
```

The `kespeech`, `cv_yue`, and `alimeeting` configurations contain contextual
evaluation JSONL records with source audio identifiers. Audio from these
external datasets is not redistributed.

### External audio mapping

| Protocol | Source mapping | Same-speaker check |
| --- | --- | --- |
| KeSpeech | Match `current_audio_id` and `history[].audio_id` to exact basenames under the official KeSpeech audio root; released basenames are unique within this evaluation set. | Both IDs share the row-level `speaker_id`, also visible as the filename prefix. |
| CV-Yue | Resolve each ID as `clips/<audio_id>` in Common Voice Cantonese 26.0. | Current and history clips share the privacy-preserving row-level `speaker_id`. |
| AliMeeting Far | Resolve `Eval_Ali_far/audio_dir/<meeting_id>_<far_channel>.wav`, then extract the current and history intervals using their respective start/end timestamps. | Both intervals belong to the target `speaker_id`; history is a same-speaker enrollment segment and need not occur earlier in the meeting. |

For AliMeeting, the reference and current clips use different derived folders
but intentionally share a basename. `current_audio_id` identifies the derived
evaluation example rather than an original SLR119 recording. The Hugging Face
dataset card gives the complete field-level mapping contract.

## Evaluation

Each benchmark record contains the current utterance, its dialogue history,
the target entity, and scenario metadata. For example:

```json
{
  "id": "0013_implicit",
  "dataset": "mm_contextasr",
  "group_id": "0013",
  "scenario": "Implicit",
  "entity": "毛虾",
  "current_audio": "audio/current/0013.wav",
  "current_audio_id": "0013.wav",
  "current_transcript": "请问毛虾一般生活在什么海域？",
  "history": [
    {
      "role": "user",
      "audio": "audio/history/0263.wav",
      "audio_id": "0263.wav",
      "text": "对虾和基围虾哪个营养价值更高？"
    },
    {
      "role": "assistant",
      "text": "对虾蛋白质含量丰富，还含有多种矿物质，基围虾则脂肪含量较低、口感更鲜嫩。两者营养价值各有优势，选择时可以根据个人口味和需求来决定。"
    }
  ],
  "language": "zh-CN",
  "split": "test",
  "task": "contextual_asr",
  "source": {
    "audio": "generated",
    "corpus": "MM-ContextASR Bench"
  }
}
```

Submit predictions as one JSON object per line, matched by `id`:

```json
{"id": "0013_implicit", "prediction": "请问毛虾一般生活在什么海域？"}
```

Run the lightweight scorer:

```bash
python evaluate.py \
  --references test.jsonl \
  --predictions predictions.jsonl
```

Use `--normalizer zh_t2s` for CV-Yue. The scorer reports CER, SER, entity
recall, and missing predictions when the corresponding annotations are
available.

## License

The code is released under [Apache-2.0](LICENSE). Dataset-specific terms are
listed on Hugging Face, and upstream licenses continue to apply to external
datasets.

## Citation

The paper link and BibTeX entry will be added when available.
