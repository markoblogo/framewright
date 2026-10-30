window.renderTrap=async function(duration=51.2){
 const bpm=150,beat=60/bpm,bar=beat*4,events=[];
 const buffer=await Tone.Offline(()=>{
  const compressor=new Tone.Compressor({threshold:-17,ratio:3,attack:.008,release:.12}),limiter=new Tone.Limiter(-1.5).toDestination();compressor.connect(limiter);
  const bassFilter=new Tone.Filter(950,'lowpass').connect(compressor),drive=new Tone.Distortion({distortion:.18,wet:.42}).connect(bassFilter);
  const bass=new Tone.Synth({oscillator:{type:'triangle'},envelope:{attack:.003,decay:.28,sustain:.40,release:.035},portamento:.055,volume:-14}).connect(drive);
  const kick=new Tone.MembraneSynth({pitchDecay:.035,octaves:5,envelope:{attack:.001,decay:.22,sustain:0,release:.05},volume:-3}).connect(compressor);
  const snareFilter=new Tone.Filter(1400,'highpass').connect(compressor);
  const claps=[0,1,2].map(()=>new Tone.NoiseSynth({noise:{type:'white'},envelope:{attack:.001,decay:.095,sustain:0,release:.035},volume:-18}).connect(snareFilter));
  const hatFilter=new Tone.Filter(6800,'highpass').connect(compressor);
  const hat=new Tone.NoiseSynth({noise:{type:'white'},envelope:{attack:.001,decay:.026,sustain:0,release:.012},volume:-25}).connect(hatFilter);
  const openHat=new Tone.NoiseSynth({noise:{type:'white'},envelope:{attack:.001,decay:.15,sustain:0,release:.04},volume:-30}).connect(hatFilter);
  const delay=new Tone.PingPongDelay({delayTime:beat*.75,feedback:.24,wet:.18}).connect(compressor);
  const lead=new Tone.PolySynth(Tone.Synth,{oscillator:{type:'triangle'},envelope:{attack:.004,decay:.28,sustain:.01,release:.35},volume:-17}).connect(delay);
  const pad=new Tone.PolySynth(Tone.Synth,{oscillator:{type:'sine'},envelope:{attack:.9,decay:.5,sustain:.20,release:1.5},volume:-28}).connect(compressor);
  const notes=['F1','F1','Ab1','Eb1'];
  for(let b=0;b<32;b++){
   const t=b*bar+.04;if(t>=duration-.6)break;const intro=b<4,bridge=b>=12&&b<16,outro=b>=28;
   if(b%4===0)pad.triggerAttackRelease(['F3','Ab3','C4'],bar*3,t,.6);
   const leadNotes=b%4===2?['Eb5','C5','Ab4']:['F4','C5','Ab4'];
   for(const [j,p] of [[0,0],[1,1.5],[2,3.25]])if((b%2===0||!intro)&&(!outro||b<30)){const at=t+p*beat;if(at<duration-.4)lead.triggerAttackRelease(leadNotes[j],beat*.32,at,.65+(j===0?.12:0));}
   if(!bridge){
    const offsets=intro?[0]:b%4===3?[0,.75,1.5,2.75,3.5]:[0,1.75,3.0];
    for(let k=0;k<offsets.length;k++){const p=offsets[k];const at=t+p*beat;if(at<duration-.3){kick.triggerAttackRelease('F1',beat*.2,at,.85);if(!intro)bass.triggerAttackRelease(notes[b%4],beat*Math.min(p===0?1.25:.55,((offsets[k+1]??4)-p)*.65),at,.70);events.push({kind:'kick',time:at});}}
    for(let c=0;c<3;c++){const at=t+2*beat+c*.011;if(at<duration-.2)claps[c].triggerAttackRelease(.045,at,c===0?.8:.5);}
    const hatGrid=new Map();for(let h=0;h<8;h++)hatGrid.set((h/2).toFixed(4),h%2===0?.65:.39);
    if(!intro&&!outro&&b%4===3)for(let h=0;h<6;h++)hatGrid.set((3.25+h/8).toFixed(4),.31+h*.04);
    for(const [p,v] of [...hatGrid].sort((a,b)=>+a[0]-+b[0])){const at=t+Number(p)*beat;if(at<duration-.2)hat.triggerAttackRelease(.007,at,v);}
    if(b%2===1&&!outro)openHat.triggerAttackRelease(.08,t+3.5*beat,.48);
   }else if(b%2===0){kick.triggerAttackRelease('F1',beat*.2,t,.6);events.push({kind:'break-hit',time:t});}
  }
 },duration,2,48000);
 const channels=buffer.toArray(),n=channels[0].length,data=new ArrayBuffer(44+n*4),view=new DataView(data),write=(at,s)=>{for(let i=0;i<s.length;i++)view.setUint8(at+i,s.charCodeAt(i));};write(0,'RIFF');view.setUint32(4,36+n*4,true);write(8,'WAVE');write(12,'fmt ');view.setUint32(16,16,true);view.setUint16(20,1,true);view.setUint16(22,2,true);view.setUint32(24,48000,true);view.setUint32(28,192000,true);view.setUint16(32,4,true);view.setUint16(34,16,true);write(36,'data');view.setUint32(40,n*4,true);let peak=0;
 for(let i=0;i<n;i++){let fade=Math.min(1,i/(48000*.025),(n-i)/(48000*.5));for(let c=0;c<2;c++){const value=channels[c][i]*fade;peak=Math.max(peak,Math.abs(value));view.setInt16(44+(i*2+c)*2,Math.round(Math.max(-1,Math.min(1,value))*32767),true);}}
 let binary='';const bytes=new Uint8Array(data);for(let i=0;i<bytes.length;i+=32768)binary+=String.fromCharCode(...bytes.subarray(i,i+32768));return {wav:btoa(binary),metadata:{bpm,duration,sampleRate:48000,channels:2,peak,events,seed:30102026,genre:'original instrumental minimal fashion trap',tone:Tone.version}};
};
