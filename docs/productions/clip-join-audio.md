# Why Is That Beep Late?

The owner accepted one 36.6-second English YouTube edit on 23 November 2026.
The package contains the accepted 1280×720, 30 fps H.264/AAC master,
a cover derived from the opening art and separate English SRT captions.
The owner supplied the [published YouTube link](https://youtu.be/nhOBQe4YgBU) on
23 November 2026 (`owner_provided_url`). YouTube oEmbed returned “Audio Out of
Sync After Joining Clips? Check the Cut” and “ABV — AI · Books · Validation”.
The updated local copy includes the standard brand footer and hashtags.
YouTube’s live description and visibility setting were not checked.

The first pilot showed two separate passes. The owner asked for generated
imagery and real footage, plus a comparison showing both versions on one
screen. The finished edit retains each solo pass and replays the pictures
side by side with one audio version audible at a time. It opens with an
authored studio still and [cottonbro studio’s clapperboard footage](https://www.pexels.com/video/a-clapper-board-used-when-shooting-a-scene-on-film-making-3945485/),
used as context under the [Pexels license](https://www.pexels.com/license/).
A second generated studio still closes on a fade to black.

## The test

Clip A has 2.00 s of picture and 2.32 s of audio. Clip B contains a simultaneous
picture flash and beep. Both variants convert footage to a common frame rate
and audio format. The first run assembles the picture and audio independently
and carries the extra 320 ms of Clip A into Clip B's audio. The second run
trims the audio to the intended edit point.

The decoded split-screen MP4 measured 320.27 ms before the fix and 0.27 ms
after, against a one-frame tolerance of 33.33 ms. The detector compares the
first bright central frame and a threshold-based audio onset, so digital
subframe readings describe this fixture only. The synthetic pair does not
show a general failure caused by mixed frame or sample rates. FFmpeg and
local composition produced the edit. ComfyUI Concatenate Video and FilmCraft
were outside the executed test. The private studio package retains the fixture,
commands, timings and export receipt.
