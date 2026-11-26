# REVERSE-STYLE-01 — known-edit comparison

26 November 2026. Owner selected analysis of a known montage. Bounded comparison complete; full semantic pipeline remains unqualified. No new film, paid service, upload, model/dependency installation, or modification of published masters.

## Input and executed route

Used our existing28s LongCat YouTube v2:1920×1080,25fps,700frames,English narration,source voice,pulse bed,editorial labels and digital camera moves. This is an authored montage with a retained recipe,not a claim to have reconstructed an external famous filmmaker's edit. Master SHA256:`28857dfe369d7bf99b146687e628fdf58a4058099220beaa4fcb6b3719a58a44`.

Primary upstream: https://github.com/kelano86/reverse-video/tree/793b80352dea379579c949b8f194da1cd01f863d . Native `measure.py`/`common.py` executed unchanged using the existing REA Python3.12.8/OpenCV/NumPy/Pillow environment. A retained wrapper supplies the already-owned YuNet model path and blocks network access;zero network attempts. No executable provider was installed. Code MIT; optional model licences remain separate. `listen.py`/style format were inspected but listening models were not executed.

Existing analysis discovery application reviewed;none of the four current ranking profiles covers reverse analysis,so no production rank/provider promotion follows. One job,external disk only. Run28.7s as reported by upstream,not a repeated benchmark. Initial available space~16GiB internal/~101GiB Work;no internal media scratch.

## Known answer versus upstream output

| Test | Result | Interpretation |
|---|---|---|
| Six authored scene boundaries |7.44,10.44,14.16,16.16,19.88,23.60s:all exact,0frame error |6/6 recall on this sample,not general accuracy.|
| Extra detections |3.72 and27.32s |Actual source-loop seams inside authored scenes,not additional story edits. Treating all8events as authored cuts gives6/8 precision.|
| Digital push10.44–14.16 |`push in` |Direction agrees with recipe.|
| Digital pull16.16–19.88 |`handheld push/pull`;entry called`punch x1.333` |Cannot establish actual handheld capture or authored zoom scale from this. Recipe is digital zoom-out.|
| Fixed split-screen and fixed crops |Often`push in`;end`pan/slide` |Subject motion/fade confounded with camera. Tool reports66.4%push time;recipe only has one3.72s dedicated push.|
| Face detector |91.1%sampled frames;two-plus38.4% |Candidates include split-screen and diagram thumbnails,not a count of actors/camera angles. No detection recall study.|
| Audio level |−16.6LUFS,LRA6.7LU,true peak−1.1dBFS |Actual mixed-audio EBU R128 numbers;no listening/voice-quality claim.|
| Boards/palette |Shot board,palette,pacing map written;operator viewed actual shot board |Useful navigation;not an assessment of original film quality.|

The comic section is a blend-in/blend-out within the2s authored segment. Correct segment boundaries do not prove the internal dissolve/easing was recovered. No reverse reconstruction rendered and no easing inferred.

## Explicit missing branches

- Native OCR attempted;`rapidocr_onnxruntime` absent. No automatic label/timing recognition demonstrated.
- Native transcription attempted;`faster_whisper` absent. Upstream writes`speech.words=0`after the import error;this is **unavailable**,not silence or an empty verified transcript.
- Stems explicitly off. With stems off and no recognised speech words the native music/SFX function returns empty;`audio={}`/`sfx=null`do not mean no music or effects. The recipe contains a pulse bed. SciPy is also absent in this environment.
- AST/CLAP semantic listening not launched:torch/transformers absent;upstream documents first-run model downloads. No SFX names,genre,mood,tempo or voice character verified. No download was needed to answer the bounded access question.
- `style.json` was **operator-curated** using native measurements and separately labelled recipe facts. Upstream provides a format/reference,not automatic evidence for every field. No captions,font identification,ASR or heard labels fabricated. No clean-machine portability or template replay claim.

## Retained evidence and reuse decision

Private trial:`/Volumes/Work/Work/FramewrightStudio/productions/reverse-style-known-edit-2026-11-26/`.

- `source/`:pinned reviewed code/reference/licence;hashes in`evidence/comparison.json`.
- `probe.py`, `evidence/measure.log`, `evidence/network-guard.json`:actual run and warnings.
- `run/measures.json`, `run/summary.md`, `run/img/shots_01.jpg`:native output. Input is a symlink to protected master,not a second production copy.
- `compare.py`, `evidence/comparison.json`, `style.json`:explicit known boundaries,source-loop accounting,camera counterexamples,curated style facts with provenance/confidence.
- Authoritative edit:`productions/radar-12-longcat-full-2026-11-26/edit/v2/render.py`;exact source and recipe hashes retained in comparison receipt.

Decision:retain reverse-video as a **manual boundary/navigation assistant**,with useful local measurements on this material. Do not use camera labels as authored instructions or missing audio/text branches as negative findings. Five visual-quality axes/owner review of this trial are not inferred from technical execution. No resource-cost estimate beyond no paid calls and one local run.

REVERSE-STYLE-01 closes this bounded comparison with partial tool coverage. Full OCR/ASR/listening needs an explicitly selected follow-up,reviewed dependencies and model/storage route;it is not silently passed or added as a new queue family. MUSIC-CUE-01 remains the sole active shortlist task and has not started. Accepted films/publication states and existing pauses remain intact.
