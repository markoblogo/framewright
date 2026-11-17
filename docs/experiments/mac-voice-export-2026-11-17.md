# Mac narration export without the tablet

17November2026. Owner authorised a Mac-only speech preflight, alternative narration tests and, if an eligible route worked, AUTOPROD test3 without intermediate approvals/download requests. No tablet was connected or used;no new paid API,account grant or public upload.

## Observed routes

- **AI Studio / Fola:** normal authenticated Chrome UI displayed Gemini3.8 Flash TTS and no API key selected. A new24-word script produced a displayed8s result. Download opened a native Save panel with Save disabled. Folder/keyboard actions did not establish a saved file;the supported browser download event timed out. Browser/native focus differed during inspection,so this does not prove the cause is a Google export defect. No hidden audio/blob extraction or browser-security workaround. Monetary UI cost not displayed. **Generation observed;autonomous Mac export not completed.**
- **ZONOS3-Mini browser playground:** the official page displayed Loading the in-browser engine;subsequent control timed out and reset. **No completed inference or export**;not a verdict on voice quality or Mac compatibility. No weights/location beyond browser cache were verified.
- **Kokoro local ONNX:** official wrapper0.6.1,ONNX Runtime1.32.0,modelv1.0 and bundled voice file downloaded to external Work. Original same-script probes produced af_heart8.8213s and af_bella9.0446s24kHzmono PCM WAVs,with nonzero nonclipped samples. Per-probe inference17.09s/19.02s after model load16.45s;download/setup/operator time are excluded and not a speed comparison with AI Studio. Actual files/hashes retained. No voice cloning or reference upload.

The owner requested alternative Mac tests. Operator selected **af_heart**,explicitly distinguished from Fola,for the [third autonomous production](../productions/agent402-tabletop.md). Seven separately generated phrases total about51.39s including lead/interphrase pauses. Whisper small CPU transcript retained: core story,Agent402 and429 recovered;the closing question has an ASR mismatch. This is content corroboration,not independent pronunciation,listening or naturalness approval. At this preflight checkpoint owner voice listening remained pending;the later17November scoped listening decision is recorded below. No stock Supertonic fallback was used.

## Reusable scope and limits

Direct local WAV export removes the browser download/dialog dependency for these selected English voices on this Mac. It does not reproduce Fola,qualify Ukrainian,multispeaker acting,other devices or every script. Model/wrapper and voice preferences remain separate. The original full voice and normalized/mixed derivatives are retained;no destructive replacement of accepted historical voices.

Private receipts: studio records/mac-voice-2026-11-17 contains browser-results.json,kokoro-probe.json,exact short script/probe.py and two WAVs. Full-film voice source,timing,Whisper output and stems stay in the existing native Agent402 production. External shared environment tools/python/kokoro-onnx and tools/models/kokoro-onnx-v1;no heavy internal scratch. Wrapper MIT and model Apache2.0 metadata reviewed;this is not blanket clearance of external recordings or a new account licence.

Primary references: [official wrapper](https://github.com/thewh1teagle/kokoro-onnx),[model card](https://huggingface.co/hexgrad/Kokoro-82M),[ZONOS model](https://huggingface.co/Zyphra/ZONOS3-Mini).

## Owner listening -17November2026

Owner explicitly called the film voice good and the alternative short voices usable. af_heart full take and both short probes now have scoped owner listening acceptance in the native project. This does not establish Fola equivalence,multilingual quality or every future take. The film has separate requested visual/player/brand corrections;voice acceptance is retained across those changes because the narration source is unchanged.
