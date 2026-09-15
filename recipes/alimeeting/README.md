# AliMeeting Far-Far v4 evaluation recipe

The release contains 2,850 overlapping target-speaker segments from the official
AliMeeting Eval split. Current audio is far-field multi-speaker speech. Historical
audio is a temporally disjoint, non-overlapping far-field segment from the same
speaker, meeting, and channel.

Obtain AliMeeting from OpenSLR SLR119 and reconstruct both segments using
`meeting_id`, `far_channel`, and the provided timestamps. Score only the target
speaker reference in `current_transcript`.
