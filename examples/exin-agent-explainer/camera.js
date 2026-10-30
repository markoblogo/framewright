(async()=>{
 const W=1920,H=1080,D=window.EXIN_TIMING,beats=D.phrases;
 const app=new PIXI.Application();await app.init({width:W,height:H,backgroundColor:0x132127,preference:'webgl',autoStart:false,sharedTicker:false,antialias:true,preserveDrawingBuffer:true});document.getElementById('source-camera').appendChild(app.canvas);
 const lab=await PIXI.Assets.load('assets/lab.jpg'),ui=await PIXI.Assets.load('assets/interface.jpg');
 const photo=new PIXI.Sprite(lab),g=new PIXI.Graphics(),detailLayer=new PIXI.Container(),lines=new PIXI.Graphics();app.stage.addChild(photo,g,detailLayer,lines);
 const tex=(x,y,w,h)=>new PIXI.Texture({source:ui.source,frame:new PIXI.Rectangle(x,y,w,h)});
 const details={people:tex(0,536,1280,230),gates:tex(880,538,400,230),sonnet:tex(875,35,405,500)};
 const detail=new PIXI.Sprite(details.people);detailLayer.addChild(detail);const outline=new PIXI.Graphics();detailLayer.addChild(outline);
 const cfg={hook:[640,450,1280,800,490,1000],claim:[650,450,1180,440,420,920],choice:[800,450,1260,860,460,1160],rig:[800,450,1120,920,520,950],people:[640,384,1280,640,405,1200],gates:[640,384,1280,680,420,1160],models:[730,450,1250,780,470,1150],sonnet:[760,460,1250,820,480,1160],outcome:[800,550,1150,830,575,1080],meaning:[820,470,1180,750,450,1240],end:[740,450,1200,640,455,1280]};
 const clamp=x=>Math.max(0,Math.min(1,x));const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
 function render(t){
  const b=beats.find(x=>t>=x.start&&t<x.start+x.duration)||beats[beats.length-1],u=clamp((t-b.start)/b.duration),a=cfg[b.id],z=smooth(u),cx=a[0]+(a[3]-a[0])*z,cy=a[1]+(a[4]-a[1])*z,cw=a[2]+(a[5]-a[2])*z,scale=W/cw;
  photo.texture=['people','gates'].includes(b.id)?ui:lab;photo.scale.set(scale);photo.position.set(W/2-cx*scale,H/2-cy*scale);g.clear();lines.clear();detailLayer.visible=false;
  if(details[b.id]){
   detailLayer.visible=true;detail.texture=details[b.id];let box=b.id==='people'?[100,495,1720,309]:b.id==='gates'?[1050,445,760,437]:[1115,105,700,864];
   const enter=smooth((t-b.start)/.55);detailLayer.position.set(box[0]+30*(1-enter),box[1]);detailLayer.alpha=enter;detail.width=box[2];detail.height=box[3];outline.clear().rect(-5,-5,box[2]+10,box[3]+10).stroke({width:4,color:0x79d3ca});
  }
  if(b.id==='claim'){
   // A source-anchored bracket highlights the computer display, not a fictional readout.
   const x=(180-cx)*scale+W/2,y=(235-cy)*scale+H/2;
   lines.rect(x,y,480*scale,265*scale).stroke({width:4,color:0x76d7cf,alpha:smooth(u*3)});
  }
  if(b.id==='choice'){
   // Explicit illustrative paper stack; no invented article title, chart or citation.
   const n=Math.min(3,Math.floor(u*5)+1);
   for(let i=0;i<n;i++){let x=160+i*115,y=555-i*22;g.roundRect(x,y,200,260,5).fill({color:0xf2f6f3,alpha:.96});for(let j=0;j<5;j++)g.rect(x+24,y+35+j*32,135-(j%2)*30,6).fill(0x87aaa7);}
   lines.moveTo(600,675).lineTo(790,675).lineTo(767,660).moveTo(790,675).lineTo(767,690).stroke({width:5,color:0x79d3ca});
  }
  if(b.id==='rig'){
   let x=(940-cx)*scale+W/2,y=(435-cy)*scale+H/2;lines.roundRect(x-110,y-130,260,410,14).stroke({width:4,color:0xe4a2c8,alpha:.9});
  }
  if(b.id==='outcome'){
   // The supplied operation photograph stays labelled as a source photograph; no recovery footage is fabricated.
   let x=(980-cx)*scale+W/2,y=(745-cy)*scale+H/2;lines.ellipse(x,y,65*scale,55*scale).stroke({width:4,color:0x79d3ca,alpha:.8});
  }
  for(const [id,show] of [['model-opus55',b.id==='models'&&u<.49],['model-opus5',b.id==='models'&&u>=.49]])document.getElementById(id).style.opacity=show?1:0;
  app.render();window.__EXIN_FRAME={t,beat:b.id,pixi:PIXI.VERSION,renderer:app.renderer.name||app.renderer.type};
 }
 const clock={t:0},total=Number(document.getElementById('root').dataset.duration);window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.to(clock,{t:total,duration:total,ease:'none',onUpdate:()=>render(clock.t)},0);
 for(const b of beats){tl.fromTo(`#beat-${b.id} .copy`,{opacity:0,y:20},{opacity:1,y:0,duration:.35,ease:'power2.out'},b.start+.12);}
 window.__timelines["main"]=tl;window.__EXIN_READY=true;window.__EXIN_SEEK=t=>{tl.seek(t,false);render(t)};render(0);
})();
