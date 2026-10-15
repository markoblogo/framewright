import React from 'react';
import {AbsoluteFill,Composition,Img,interpolate,staticFile,useCurrentFrame} from 'remotion';
const C={ink:'#082a32',paper:'#eee5cc',gold:'#d69c36',pale:'#c6d5c5',red:'#b24d35'};
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const ease=(v:number)=>{v=clamp(v);return v*v*(3-2*v)};
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const Grain=({x,y,angle=0,s=1}:{x:number,y:number,angle?:number,s?:number})=><g transform={`translate(${x},${y}) rotate(${angle}) scale(${s})`}><ellipse rx="10" ry="23" fill={C.gold} stroke={C.ink} strokeWidth="1.5"/><path d="M0 -16 Q-3 0 0 17" stroke="#8b642a" fill="none"/></g>;
const Title=({children,top=125,size=72}:{children:React.ReactNode,top?:number,size?:number})=><div style={{position:'absolute',left:110,top,fontSize:size,fontWeight:850,lineHeight:1.12,letterSpacing:-1.6,maxWidth:1620}}>{children}</div>;
function Film(){const f=useCurrentFrame(),t=f/30;const route=ease((t-6.3)/2),contract=ease((t-11.4)/1.8),reveal=ease((t-15.5)/1.2);const bob=Math.sin(t*1.6)*6;
return <AbsoluteFill style={{background:C.paper,color:C.ink,fontFamily:'Arial, sans-serif',overflow:'hidden'}}>
<svg width="1920" height="1080" style={{position:'absolute',inset:0}}>
<defs><pattern id="paper" width="13" height="13" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r=".7" fill={C.ink} opacity=".05"/></pattern><filter id="shadow"><feDropShadow dx="0" dy="14" stdDeviation="12" floodOpacity=".18"/></filter></defs>
<rect width="1920" height="1080" fill="url(#paper)"/>
<g opacity={1-reveal}>
<path d={`M-80 ${790-route*160} Q400 ${490+route*100} 850 ${780-route*150} T2000 680 L2000 1200 L-80 1200Z`} fill={C.pale}/>
<path d={`M-80 920 Q650 ${570+route*80} 1250 780 T2100 650 L2000 1200 L-80 1200Z`} fill={C.ink}/>
<path d="M300 730 C650 450 1150 980 1610 510" fill="none" stroke={C.gold} strokeWidth="6" strokeDasharray="13 18" opacity={route*(1-contract)}/>
{Array.from({length:90},(_,i)=>{const row=Math.floor(i/15),col=i%15;const gx=150+col*118+Math.sin(row)*25,gy=520+row*54+Math.sin(col*.6)*36;const a=i/89;const rx=300+1310*a,ry=730-220*a+Math.sin(a*Math.PI*2)*130;const cx=650+col*50,cy=440+row*34;return <Grain key={i} x={lerp(lerp(gx,rx,route),cx,contract)} y={lerp(lerp(gy+bob,ry,route),cy,contract)} angle={lerp(lerp(-25+Math.sin(i)*20,55,route),90,contract)} s={lerp(1,.48,contract)}/>})}
<g opacity={route*(1-contract)} filter="url(#shadow)">
<path d="M150 730 L150 570 L240 495 L330 570 L330 730Z" fill={C.paper} stroke={C.ink} strokeWidth="5"/><path d="M175 580 H305 M175 615 H305 M175 650 H305" stroke={C.gold} strokeWidth="6"/>
<g transform={`translate(${lerp(450,1280,ease((t-8)/3.3))},735)`}><path d="M-110 -90 H35 V-40 H110 V30 H-110Z" fill={C.red} stroke={C.paper} strokeWidth="5"/><path d="M45 -35 V-80 H85 L110 -35Z" fill={C.gold}/><circle cx="-65" cy="35" r="27" fill={C.ink} stroke={C.paper} strokeWidth="9"/><circle cx="70" cy="35" r="27" fill={C.ink} stroke={C.paper} strokeWidth="9"/></g>
<g transform="translate(1510 475)"><path d="M-70 95 H180 L130 165 H-35Z" fill={C.red} stroke={C.ink} strokeWidth="4"/><path d="M0 95 V-50 H80 V95" fill={C.paper} stroke={C.ink} strokeWidth="4"/><path d="M90 90 V-160 H165 M90 -160 L155 -60" fill="none" stroke={C.ink} strokeWidth="10"/></g>
</g>
<g opacity={contract} transform={`translate(${lerp(0,55,contract)} ${lerp(70,0,contract)}) rotate(${lerp(-8,-3,contract)} 960 610)`} filter="url(#shadow)"><rect x="500" y="360" width="850" height="440" rx="8" fill={C.paper} stroke={C.ink} strokeWidth="3"/><text x="565" y="423" fontSize="36" fontWeight="bold" fill={C.ink}>УГОДА — ЦЕ СИСТЕМА</text><path d="M560 475 H1290 M560 550 H1290 M560 625 H1290" stroke={C.ink} strokeWidth="2" opacity=".2"/><text x="560" y="520" fontSize="31" fill={C.ink}>Товар · Якість · Ціна · Логістика</text><text x="560" y="597" fontSize="31" fill={C.ink}>Контракт · Ризик · Наступна дія</text><g transform={`translate(1190 710) rotate(-12) scale(${lerp(1.8,1,ease((t-13.7)/.4))})`} opacity={ease((t-13.7)/.15)}><rect x="-110" y="-40" width="220" height="80" rx="6" fill="none" stroke={C.red} strokeWidth="6"/><text textAnchor="middle" y="12" fontSize="30" fontWeight="bold" fill={C.red}>ВИКОНАННЯ</text></g></g>
</g></svg>
<div style={{position:'absolute',top:58,left:110,fontSize:23,letterSpacing:4,fontWeight:700}}>MN7R / ПРАКТИЧНИЙ ГІД</div>
{t<6.9&&<div style={{opacity:1-ease((t-6.3)/.6),transform:`translateY(${30*(1-ease(t/1.2))}px)`}}><Title>Усе починається<br/>із зерна.</Title><div style={{position:'absolute',top:335,left:114,fontSize:33,color:C.red}}>Але угода — це значно більше.</div></div>}
{t>=6.3&&t<12&&<div style={{opacity:ease((t-6.3)/.5)*(1-ease((t-11.4)/.6))}}><Title>З’єднати людей.<br/>Побудувати маршрут.</Title><div style={{position:'absolute',top:330,left:114,fontSize:32}}>Якість → Ціна → Логістика</div></div>}
{t>=11.4&&t<16.1&&<div style={{opacity:ease((t-11.4)/.5)*(1-ease((t-15.5)/.6))}}><Title>Від офера<br/>до виконання.</Title></div>}
<div style={{position:'absolute',inset:0,background:C.ink,color:C.paper,opacity:reveal,transform:`translateX(${(1-reveal)*140}px)`}}>
<svg width="1920" height="1080" style={{position:'absolute',inset:0}}><circle cx="1510" cy="560" r="610" fill="#173d44"/><circle cx="1510" cy="560" r="490" fill="none" stroke={C.gold} strokeWidth="2" opacity=".3"/>{Array.from({length:12},(_,i)=><path key={i} d={`M${80+i*160} 1080 L${600+i*150} 0`} stroke={C.gold} strokeWidth="1" opacity=".04"/>)}</svg>
<div style={{position:'absolute',left:110,top:145,fontSize:25,letterSpacing:4,color:C.gold}}>БЕЗКОШТОВНА УКРАЇНСЬКА ВЕРСІЯ</div>
<div style={{position:'absolute',left:110,top:235,fontSize:76,fontWeight:850,lineHeight:1.08,width:970}}>Брокеридж<br/>на ринках зернових<br/>та олійних</div>
<div style={{position:'absolute',left:114,top:535,fontSize:35,color:'#b8ceca'}}>Практичний гід для брокерів</div>
<div style={{position:'absolute',left:110,top:660,display:'flex',gap:20}}>{['PDF','EPUB','УКРАЇНСЬКОЮ'].map(x=><div key={x} style={{fontSize:26,padding:'14px 24px',border:`2px solid ${C.gold}`,color:C.gold}}>{x}</div>)}</div>
<div style={{position:'absolute',left:112,top:825,fontSize:39,fontWeight:700}}>Завантажуйте та читайте</div><div style={{position:'absolute',left:114,top:892,fontSize:30,color:C.gold}}>abvx.xyz · Розділ «Книги»</div>
<Img src={staticFile('book.jpeg')} style={{position:'absolute',width:700,height:900,objectFit:'cover',objectPosition:'57% center',right:60,top:90,boxShadow:'0 26px 60px #0008',transform:`perspective(1400px) rotateY(${-9+reveal*3}deg) rotateZ(2deg) scale(${.94+.06*ease((t-15.5)/4)})`}}/>
</div>
<div style={{position:'absolute',bottom:42,left:110,fontSize:22,letterSpacing:2,color:t<15?C.paper:C.gold}}>ЛЮДИ · ТОВАР · ЛОГІСТИКА · ЦІНА · УГОДА</div>
<div style={{position:'absolute',bottom:0,left:0,height:6,width:`${f/719*100}%`,background:C.gold}}/>
</AbsoluteFill>}
export const Root=()=> <Composition id="AgroUK" component={Film} durationInFrames={720} fps={30} width={1920} height={1080}/>;
