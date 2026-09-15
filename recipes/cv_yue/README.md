# CV-Yue evaluation recipe

The release uses the official Cantonese test split from Mozilla Common Voice
26.0 (3,525 utterances). Each current utterance is paired with another utterance
from the same speaker and split. The pairing is fixed across context modes.

Resolve `current_audio_id` and historical `audio_id` against the `yue/clips`
directory. Convert both predictions and references with OpenCC `t2s` before
Chinese CER and SER normalization.
