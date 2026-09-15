# Data schema

Each line is a self-contained canonical evaluation example. The schema stores
source identifiers, not audio bytes or machine-specific paths.

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable release identifier. |
| `dataset` | string | Track name. |
| `split` | string | Official source split. |
| `task` | string | `contextual_asr`, `asr`, or `target_speaker_asr`. |
| `language` | string | BCP-47 language tag. |
| `current_audio_id` | string | Source audio or segment identifier. |
| `current_transcript` | string | Current-turn reference; never model input. |
| `history` | list | Ordered historical user/assistant turns. |
| `source` | object | Source corpus, release, and identifier namespace. |

Optional task fields include `entity`, `confusion_term`, `scenario`,
`group_id`, `speaker_id`, `accent`, `meeting_id`, timing, and overlap metadata.

Audio identifiers must be resolved against a legally obtained source dataset.
Absolute paths, internal object-store URIs, signed URLs, and credentials are
invalid release fields.
