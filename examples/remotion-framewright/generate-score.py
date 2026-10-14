"""Original deterministic instrumental, no sampled or third-party music."""
from array import array
from math import sin, pi, exp
from pathlib import Path
import wave
rate=48000
length=30
out=array('h')
chords=[(146.83,174.61,220),(130.81,164.81,196),(110,130.81,164.81),(130.81,174.61,220),(146.83,174.61,220)]
for i in range(rate*length):
    t=i/rate
    chord=chords[min(int(t/6),4)]
    pad=sum(sin(2*pi*f*t)+.17*sin(4*pi*f*t) for f in chord)*.026
    step=int(t/.4)
    note=chord[step%3]*2
    age=t%.4
    pluck=(sin(2*pi*note*t)+.15*sin(4*pi*note*t))*exp(-age*11)*.055
    beat=t%.8
    bass=sin(2*pi*chord[0]/2*t)*exp(-beat*9)*.07
    fade=min(1,t/1.2,max(0,(length-t)/2.2))
    left=(pad+pluck+bass)*fade
    right=(pad+pluck*.87+bass+.008*sin(2*pi*chord[1]*t+.4))*fade
    out.extend([int(max(-.98,min(.98,left))*32767),int(max(-.98,min(.98,right))*32767)])
with wave.open(str(Path('outputs/framewright-score-original.wav')),'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(rate); w.writeframes(out.tobytes())
