function presenterTile(id,frame,x,y,w,h){const im=portraits[id];g.drawImage(im,(frame%3)*512,Math.floor(frame/3)*512,512,512,x,y,w,h)}
function hosts(t){
 const show=ease((t-.12)/.38)*(1-ease((t-8.45)/.5));if(show<=0)return;
 const q=timeline.turns.find(v=>t>=v.start&&t<v.end),amp=env[Math.min(env.length-1,Math.floor(t*60))]||0;
 g.save();g.globalAlpha=show;
 for(let k=0;k<2;k++){
  const active=q?.speaker===(k===0?'A':'B'),color=k===0?pink:teal,x=1296+k*280,y=522+(1-show)*22,w=260;
  box(x-3,y-3,w+6,312,active?color:'#658388',18);g.save();g.beginPath();g.roundRect(x,y,w,260,15);g.clip();
  let pose=active?(amp<.12?0:amp<.34?1:Math.floor(t*8)%3===0?3:2):5;
  if((k===0&&t>2.65&&t<2.79)||(k===1&&t>6.85&&t<6.99))pose=4;
  const scale=1.025+.003*Math.sin(t*2+k),s=w*scale,dx=x+(w-s)/2,dy=y+(260-s)/2+Math.sin(t*1.4+k)*.6;
  const beat=Math.floor(t*12),phase=t*12-beat,prevTime=Math.max(0,(beat-1)/12),prevAmp=env[Math.min(env.length-1,Math.floor(prevTime*60))]||0;
  let prev=active?(prevAmp<.12?0:prevAmp<.34?1:Math.floor(prevTime*8)%3===0?3:2):5;if(pose===4)prev=4;
  const id=k===0?'questioner':'maker';presenterTile(id,prev,dx,dy,s,s);g.globalAlpha=show*ease(phase/.6);presenterTile(id,pose,dx,dy,s,s);g.globalAlpha=show;g.restore();
  box(x,y+250,w,56,'#172b33',0);txt(k===0?'THE QUESTION':'THE MAKER',x+16,y+263,21,color,700);
  if(active){g.fillStyle=color;g.beginPath();g.arc(x+w-22,y+278,5+amp*3,0,Math.PI*2);g.fill()}
 }
 txt('AI PRESENTERS',1298,492,17,'#f6efdb',600);g.restore();
}
