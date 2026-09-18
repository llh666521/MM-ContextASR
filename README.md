<div align="center">

# MM-ContextASR

### Multimodal Conversational Context for LLM-Based ASR

[![GitHub stars](https://img.shields.io/github/stars/llh666521/MM-ContextASR?style=flat&logo=github)](https://github.com/llh666521/MM-ContextASR/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/llh666521/MM-ContextASR)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench)
[![arXiv](https://img.shields.io/badge/arXiv-2609.19765-b31b1b?logo=arxiv)](https://arxiv.org/abs/2609.19765)
[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-29966F)](LICENSE)

[Paper](https://arxiv.org/pdf/2609.19765) · [Data Pipeline](#data-pipeline) · [Context Training](#context-training) ·
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

<table>
  <thead>
    <tr>
      <th align="center">Training</th>
      <th align="center">Context</th>
      <th align="center">Irrelevant ↑</th>
      <th align="center">Implicit ↑</th>
      <th align="center">Explicit ↑</th>
      <th align="center">Correction ↑</th>
      <th align="center">Repeated<br>Error ↑</th>
      <th align="center">Overall ↑</th>
    </tr>
  </thead>
  <tbody>
    <tr><th colspan="8" align="center">Qwen3-Omni-Instruct</th></tr>
    <tr><td rowspan="4" align="center"><strong>Base</strong></td><td align="center">No Context</td><td align="center">74.00</td><td align="center">74.00</td><td align="center">74.00</td><td align="center">74.00</td><td align="center">74.00</td><td align="center">74.00</td></tr>
    <tr><td align="center">Text-only</td><td align="center">68.40</td><td align="center">74.00</td><td align="center">95.60</td><td align="center">96.00</td><td align="center">67.60</td><td align="center">80.32</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">65.60</td><td align="center">74.40</td><td align="center">92.40</td><td align="center">96.40</td><td align="center">72.00</td><td align="center">80.16</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">69.60</td><td align="center">77.60</td><td align="center">97.60</td><td align="center">97.60</td><td align="center">71.60</td><td align="center">82.80</td></tr>
    <tr><td rowspan="4" align="center"><strong>Context SFT</strong></td><td align="center">No Context</td><td align="center"><strong>76.80</strong></td><td align="center">76.80</td><td align="center">76.80</td><td align="center">76.80</td><td align="center">76.80</td><td align="center">76.80</td></tr>
    <tr><td align="center">Text-only</td><td align="center">76.40</td><td align="center">83.20</td><td align="center">97.20</td><td align="center">98.40</td><td align="center">77.20</td><td align="center">86.48</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">76.40</td><td align="center">82.40</td><td align="center">98.40</td><td align="center">98.40</td><td align="center"><strong>82.80</strong></td><td align="center">87.68</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">75.60</td><td align="center"><strong>83.60</strong></td><td align="center"><strong>98.80</strong></td><td align="center"><strong>98.80</strong></td><td align="center">82.40</td><td align="center"><strong>87.84</strong></td></tr>
    <tr><th colspan="8" align="center">Step-Audio-2-mini</th></tr>
    <tr><td rowspan="4" align="center"><strong>Base</strong></td><td align="center">No Context</td><td align="center">67.20</td><td align="center">67.20</td><td align="center">67.20</td><td align="center">67.20</td><td align="center">67.20</td><td align="center">67.20</td></tr>
    <tr><td align="center">Text-only</td><td align="center">63.20</td><td align="center">63.20</td><td align="center">93.20</td><td align="center">90.00</td><td align="center">52.80</td><td align="center">72.48</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">64.80</td><td align="center">63.20</td><td align="center">91.60</td><td align="center">89.20</td><td align="center">59.20</td><td align="center">73.60</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">64.40</td><td align="center">66.40</td><td align="center">95.60</td><td align="center">91.20</td><td align="center">53.20</td><td align="center">74.16</td></tr>
    <tr><td rowspan="4" align="center"><strong>Context SFT</strong></td><td align="center">No Context</td><td align="center"><strong>72.80</strong></td><td align="center">72.80</td><td align="center">72.80</td><td align="center">72.80</td><td align="center">72.80</td><td align="center">72.80</td></tr>
    <tr><td align="center">Text-only</td><td align="center">70.80</td><td align="center">76.00</td><td align="center">96.00</td><td align="center">97.60</td><td align="center">77.40</td><td align="center">83.56</td></tr>
    <tr><td align="center">Speech-only</td><td align="center"><strong>72.80</strong></td><td align="center">75.60</td><td align="center"><strong>97.20</strong></td><td align="center"><strong>98.40</strong></td><td align="center">80.80</td><td align="center">84.96</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">72.00</td><td align="center"><strong>76.80</strong></td><td align="center">96.80</td><td align="center"><strong>98.40</strong></td><td align="center"><strong>82.00</strong></td><td align="center"><strong>85.20</strong></td></tr>
  </tbody>
</table>

### Accent and Dialect ASR

CV-Yue uses simplified-Chinese normalization.

<table>
  <thead>
    <tr><th align="center">Training</th><th align="center">Context</th><th align="center">Recall ↑</th><th align="center">CER ↓</th><th align="center">SER ↓</th></tr>
  </thead>
  <tbody>
    <tr><th colspan="5" align="center">KeSpeech</th></tr>
    <tr><td rowspan="4" align="center"><strong>Base</strong></td><td align="center">No Context</td><td align="center">80.16</td><td align="center">6.60</td><td align="center">35.58</td></tr>
    <tr><td align="center">Text-only</td><td align="center">78.78</td><td align="center">6.88</td><td align="center">36.54</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">78.73</td><td align="center">6.42</td><td align="center">36.79</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">79.13</td><td align="center">6.30</td><td align="center">36.10</td></tr>
    <tr><td rowspan="4" align="center"><strong>Context SFT</strong></td><td align="center">No Context</td><td align="center">83.71</td><td align="center">4.51</td><td align="center">29.56</td></tr>
    <tr><td align="center">Text-only</td><td align="center">83.90</td><td align="center">4.40</td><td align="center">29.14</td></tr>
    <tr><td align="center">Speech-only</td><td align="center"><strong>84.93</strong></td><td align="center">4.19</td><td align="center">28.39</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center"><strong>84.93</strong></td><td align="center"><strong>4.17</strong></td><td align="center"><strong>28.20</strong></td></tr>
    <tr><th colspan="5" align="center">CV-Yue</th></tr>
    <tr><td rowspan="4" align="center"><strong>Base</strong></td><td align="center">No Context</td><td align="center">85.32</td><td align="center">4.59</td><td align="center">30.72</td></tr>
    <tr><td align="center">Text-only</td><td align="center">81.01</td><td align="center">5.10</td><td align="center">33.67</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">81.27</td><td align="center">4.95</td><td align="center">32.68</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">83.04</td><td align="center">4.79</td><td align="center">32.28</td></tr>
    <tr><td rowspan="4" align="center"><strong>Context SFT</strong></td><td align="center">No Context</td><td align="center"><strong>88.10</strong></td><td align="center">4.89</td><td align="center">33.08</td></tr>
    <tr><td align="center">Text-only</td><td align="center">85.06</td><td align="center">4.14</td><td align="center">28.51</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">87.85</td><td align="center">3.83</td><td align="center">26.36</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">87.85</td><td align="center"><strong>3.74</strong></td><td align="center"><strong>26.33</strong></td></tr>
  </tbody>
</table>

### Target-Speaker ASR

Results on 2,850 overlapping far-field AliMeeting segments.

<table>
  <thead>
    <tr><th align="center">Training</th><th align="center">Context</th><th align="center">CER ↓</th><th align="center">SER ↓</th></tr>
  </thead>
  <tbody>
    <tr><th colspan="4" align="center">AliMeeting Far</th></tr>
    <tr><td rowspan="4" align="center"><strong>Base</strong></td><td align="center">No Context</td><td align="center">29.70</td><td align="center">82.74</td></tr>
    <tr><td align="center">Text-only</td><td align="center">31.87</td><td align="center">82.98</td></tr>
    <tr><td align="center">Speech-only</td><td align="center">33.26</td><td align="center">81.30</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">32.23</td><td align="center">81.40</td></tr>
    <tr><td rowspan="4" align="center"><strong>Context SFT</strong></td><td align="center">No Context</td><td align="center">30.25</td><td align="center">75.61</td></tr>
    <tr><td align="center">Text-only</td><td align="center">29.60</td><td align="center">74.60</td></tr>
    <tr><td align="center">Speech-only</td><td align="center"><strong>24.59</strong></td><td align="center">72.18</td></tr>
    <tr><td align="center">Speech+Text</td><td align="center">24.80</td><td align="center"><strong>71.96</strong></td></tr>
  </tbody>
</table>

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

Technical report: [arXiv:2609.19765](https://arxiv.org/abs/2609.19765)
([PDF](https://arxiv.org/pdf/2609.19765)).

```bibtex
@article{li2026multimodal,
  title   = {Multimodal Conversational Context for LLM-Based ASR: Data Construction, Training, and Benchmark},
  author  = {Li, Longhao and Tang, Jian and Kong, Yuxiang and Chen, Jie and Zhang, Binbin and Xie, Lei and Li, Xiangang},
  journal = {arXiv preprint arXiv:2609.19765},
  year    = {2026}
}
```
