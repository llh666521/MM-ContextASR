<h1 align="center">MM-ContextASR</h1>

<p align="center">
  <b>Multimodal Conversational Context for LLM-Based ASR</b><br>
  Data Construction, Training, and Benchmark
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench">Hugging Face Dataset</a>
  &nbsp;|&nbsp;
  <a href="#benchmark">Benchmark</a>
  &nbsp;|&nbsp;
  <a href="#evaluation">Evaluation</a>
  &nbsp;|&nbsp;
  <a href="#citation">Citation</a>
</p>

MM-ContextASR studies how speech and text from dialogue history help an ASR
system recognize the current utterance. The release combines a controlled
multimodal benchmark with evaluation metadata for multi-accent, Cantonese, and
target-speaker ASR.

<p align="center">
  <img src="assets/length_distribution.png" width="100%" alt="Text-length distributions in MM-ContextASR Bench">
</p>

## News

- **2026-09-15:** Released MM-ContextASR Bench metadata and 1,439 generated WAV
  files, together with the KeSpeech, CV-Yue, and AliMeeting evaluation JSONL.

## Download

All benchmark data are hosted on
[Hugging Face](https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench).

```python
from datasets import load_dataset

mm = load_dataset("lilonghao/MM-ContextASR-Bench", "mm_contextasr", split="test")
cv_yue = load_dataset("lilonghao/MM-ContextASR-Bench", "cv_yue", split="test")
kespeech = load_dataset("lilonghao/MM-ContextASR-Bench", "kespeech", split="test")
alimeeting = load_dataset("lilonghao/MM-ContextASR-Bench", "alimeeting", split="test")
```

To download the complete release, including MM-ContextASR audio:

```bash
git lfs install
git clone https://huggingface.co/datasets/lilonghao/MM-ContextASR-Bench
```

## Dataset

| Track | Test examples | Released audio | Context signal | Metrics |
| --- | ---: | --- | --- | --- |
| MM-ContextASR Bench | 1,250 | 1,439 WAV files | controlled dialogue history | entity Recall |
| KeSpeech | 19,212 | source audio IDs | multi-accent same-speaker history | CER, SER, entity Recall |
| CV-Yue | 3,525 | source audio IDs | Cantonese same-speaker history | CER, SER, entity Recall |
| AliMeeting Far-Far v4 | 2,850 | segment IDs and timestamps | far-field target-speaker history | target-only CER, SER |

The external tracks contain complete evaluation JSONL and contextual metadata,
but do not redistribute their source audio. Resolve the released audio IDs from
the corresponding upstream datasets under their original licenses.

### Record contents

Each JSONL row preserves the current audio ID, reference transcription, ordered
history, and source provenance. Track-specific fields provide scenario and
entity labels, accent, speaker or meeting IDs, timestamps, and overlap
statistics. MM-ContextASR rows additionally point to repository-relative audio
under `audio/current/` and `audio/history/`.

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

## Benchmark

### Four context settings

| Setting | Historical speech | Historical text | Assistant text |
| --- | :---: | :---: | :---: |
| No Context |  |  |  |
| Text-only |  | yes | yes |
| Speech-only | yes |  | yes |
| Speech+Text | yes | yes | yes |

### Five controlled scenarios

For each of 250 current utterances, MM-ContextASR keeps the current speech,
reference, and target entity fixed while changing only the dialogue history.

| Scenario | Historical evidence | Capability tested |
| --- | --- | --- |
| Irrelevant | unrelated topic | ignore distractors |
| Implicit | related topic without the entity | use indirect cues |
| Explicit | correct entity appears | use direct evidence |
| Correction | assistant corrects a historical ASR error | recover from errors |
| Repeated Error | assistant repeats the historical error | resist error propagation |

## Evaluation

Predictions are JSONL records with `id` and `prediction` fields. The repository
keeps evaluation intentionally lightweight:

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

The evaluation script is Apache-2.0. Dataset terms are listed per configuration
in the Hugging Face release. External source licenses continue to apply.

## Citation

The paper and BibTeX entry will be added when the public identifier is ready.

