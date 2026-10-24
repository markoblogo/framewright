/* Original bounded browser runner. No installs, persistent profile or hosting. */
const fs=require('fs'), path=require('path');
const [configPath,out,browserPath,modulePath]=process.argv.slice(2);
const cfg=JSON.parse(fs.readFileSync(configPath,'utf8'));
const puppeteer=require(modulePath);
const delay=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const browser=await puppeteer.launch({executablePath:browserPath,headless:true,args:['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding',...cfg.browser_args]});
 const watchdog=setTimeout(async()=>{await browser.close();process.exitCode=1;},(cfg.duration_seconds+cfg.timeout_seconds*4+30)*1000);
 const errors=[];const report={adapter:cfg.adapter,errors,scope:'Ephemeral capture session; hosted game unchanged'};
 try{
  const page=await browser.newPage();page.setDefaultTimeout(cfg.timeout_seconds*1000);
  await page.setViewport({width:cfg.width,height:cfg.height,deviceScaleFactor:1});
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(cfg.url,{waitUntil:'domcontentloaded',timeout:cfg.timeout_seconds*1000});
  if(cfg.hook)await page.addScriptTag({content:fs.readFileSync(cfg.hook,'utf8')});
  await page.waitForFunction(adapter=>{
   const x=adapter==='playmcp'?window.PlayMCP:window.FramewrightCapture;
   return x&&typeof x.state==='function'&&x.state().ready&&document.querySelector('canvas');
  },{},cfg.adapter);
  const contract=await page.evaluate(async c=>{
   const x=c.adapter==='playmcp'?window.PlayMCP:window.FramewrightCapture;
   for(const k of ['play','pause','seek','mute','setBot','state'])if(typeof x[k]!=='function')throw Error('Missing capture method '+k);
   window.__fwController=x;
   await x.play();await x.pause();let a=x.state();await new Promise(r=>setTimeout(r,250));let b=x.state();
   if(a.playing!==false||b.playing!==false||Math.abs(b.t-a.t)>.08)throw Error('Pause does not hold scene time');
   await x.seek(c.seek_seconds);let sought=x.state();if(Math.abs(sought.t-c.seek_seconds)>.25)throw Error('Seek failed');
   await x.setBot(c.bot);if(x.state().bot!==c.bot)throw Error('Bot state failed');
   await x.play();await new Promise(r=>setTimeout(r,300));let resumed=x.state();
   if(!resumed.playing||resumed.t<=sought.t)throw Error('Resume does not advance time');
   return {paused_time_held:true,seek_verified:true,bot_verified:true,resume_verified:true};
  },cfg);
  report.controls=contract;
  const audio=await page.evaluate(async c=>{
   if(c.audio==='none'){await __fwController.mute(true);return {policy:'none',proof:'not_performed'};}
   const mixer=new AudioContext();await mixer.resume();const destination=mixer.createMediaStreamDestination();
   const links=[];
   if(c.adapter==='playmcp'){
    const sinks=__fwController.sinks();if(!sinks.length)throw Error('Native audio sinks unavailable');
    for(const gain of sinks){await gain.context.resume();const d=gain.context.createMediaStreamDestination();gain.connect(d);const src=mixer.createMediaStreamSource(d.stream);src.connect(destination);links.push({gain,d,src});}
   }else{
    if(typeof __fwController.getAudioStream!=='function')throw Error('Game audio requires getAudioStream');
    const stream=await __fwController.getAudioStream();if(!stream.getAudioTracks().length)throw Error('Game has no audio track');
    const src=mixer.createMediaStreamSource(stream);src.connect(destination);links.push(src);
   }
   const analyser=mixer.createAnalyser();analyser.fftSize=2048;
   const meter=mixer.createMediaStreamSource(destination.stream);meter.connect(analyser);
   const rms=async()=>{await new Promise(r=>setTimeout(r,180));let sum=0;const b=new Float32Array(2048);for(let i=0;i<5;i++){analyser.getFloatTimeDomainData(b);sum+=b.reduce((s,x)=>s+x*x,0)/b.length;await new Promise(r=>setTimeout(r,35));}return Math.sqrt(sum/5);};
   await __fwController.mute(false);const audible=await rms();await __fwController.mute(true);const muted=await rms();await __fwController.mute(false);const restored=await rms();
   if(audible<1e-5||restored<1e-5||muted>Math.max(1e-6,audible*.02))throw Error('Captured audio does not follow native mute/restore');
   window.__fwAudio={mixer,destination,links,meter,analyser};
   return {policy:'game',proof:'measured_capture_bus',rms:{audible,muted,restored}};
  },cfg);
  report.audio=audio;
  const source=path.join(out,'source.webm');const stream=fs.createWriteStream(source,{flags:'wx'});let chunkError;
  stream.on('error',e=>{chunkError=e;});
  await page.exposeFunction('__fwChunk',async b64=>{if(chunkError)throw chunkError;const b=Buffer.from(b64,'base64');if(!stream.write(b))await new Promise((r,j)=>{stream.once('drain',r);stream.once('error',j);});});
  try{
   report.recording=await page.evaluate(async c=>{
    const canvas=document.querySelector(c.canvas);if(!(canvas instanceof HTMLCanvasElement))throw Error('Selector must identify a canvas');
    await __fwController.seek(c.seek_seconds);await __fwController.play();
    const hook=window.FramewrightCapture;
    const started=performance.now();let raf;let active=true;
    if(hook&&typeof hook.setCaptureTime==='function'){
     const tick=()=>{if(!active)return;hook.setCaptureTime((performance.now()-started)/1000,c.duration_seconds);raf=requestAnimationFrame(tick);};tick();
    }
    const capture=canvas.captureStream(c.fps);
    if(c.audio==='game')for(const track of __fwAudio.destination.stream.getAudioTracks())capture.addTrack(track);
    const types=c.audio==='game'?['video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus']:['video/webm;codecs=vp9','video/webm;codecs=vp8'];
    const mime=types.find(t=>MediaRecorder.isTypeSupported(t));if(!mime)throw Error('No supported WebM encoder');
    const recorder=new MediaRecorder(capture,{mimeType:mime,videoBitsPerSecond:8000000});let chain=Promise.resolve();
    recorder.ondataavailable=e=>{if(!e.data.size)return;chain=chain.then(async()=>{const bytes=new Uint8Array(await e.data.arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=32768)s+=String.fromCharCode(...bytes.subarray(i,i+32768));await __fwChunk(btoa(s));});};
    try{return await new Promise((resolve,reject)=>{
     recorder.onerror=e=>reject(Error(e.error?.message||'MediaRecorder failed'));
     recorder.onstop=()=>chain.then(()=>resolve({mime,wall_seconds:(performance.now()-started)/1000}),reject);
     recorder.start(500);setTimeout(()=>{if(recorder.state!=='inactive')recorder.stop();},c.duration_seconds*1000);
    });}finally{active=false;cancelAnimationFrame(raf);capture.getTracks().forEach(t=>t.stop());}
   },cfg);
  }finally{await new Promise((r,j)=>stream.end(e=>e?j(e):r()));}
  await page.screenshot({path:path.join(out,'end.png')});
  if(errors.length)throw Error('Page errors during recording');
 }catch(e){report.error=String(e);throw e;}finally{clearTimeout(watchdog);fs.writeFileSync(path.join(out,'browser-report.json'),JSON.stringify(report,null,2));await browser.close();}
})().catch(e=>{process.stderr.write(String(e)+'\n');process.exitCode=1;});
