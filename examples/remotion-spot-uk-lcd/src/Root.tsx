import React from 'react';
import {AbsoluteFill,Composition,Img,staticFile,useCurrentFrame} from 'remotion';
const C={ink:'#172016',lcd:'#a2ac78',light:'#d6d9ac',gold:'#d7aa3b',case:'#343d2b'};
const e=(v:number)=>{v=Math.min(1,Math.max(0,v));return v*v*(3-2*v)};
const mix=(a:number,b:number,p:number)=>a+(b-a)*p;
const alpha=(t:number,a:number,b:number)=>e((t-a)/.35)*(1-e((t-b)/.35));
const patterns:Record<string,string[]>= {S:['11111','10000','10000','11111','00001','00001','11111'],P:['11110','10001','10001','11110','10000','10000','10000'],O:['01110','10001','10001','10001','10001','10001','01110'],T:['11111','00100','00100','00100','00100','00100','00100']};
const Pixels=({word,x,y,size=12}:{word:string,x:number,y:number,size?:number})=><g>{word.split('').map((a,i)=>(patterns[a]||[]).map((row,j)=>row.split('').map((v,k)=>v==='1'?<rect key={`${i}-${j}-${k}`} x={x+(i*6+k)*size} y={y+j*size} width={size-2} height={size-2} rx="1" fill={C.ink}/>:null)))}</g>;
function Film(){const t=useCurrentFrame()/30;const close=e((t-13.1)/.7);const question=1-e((t-4.1)/.25);const factors=alpha(t,4.15,9.3);const supply=alpha(t,9.35,12.85);
return <AbsoluteFill style={{background:C.ink,fontFamily:'Arial, sans-serif',color:C.ink,overflow:'hidden'}}>
<svg width="1920" height="1080" style={{position:'absolute',inset:0}}>
<defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.5" height="1.5" fill={C.ink} opacity=".12"/></pattern></defs>
<rect x="48" y="44" width="1824" height="992" rx="54" fill={C.case}/><rect x="76" y="72" width="1768" height="936" rx="36" fill="#0a100b"/><rect x="100" y="97" width="1720" height="886" rx="22" fill={C.lcd}/><rect x="100" y="97" width="1720" height="886" rx="22" fill="url(#grid)"/>
{Array.from({length:20},(_,i)=><rect key={i} x={120+i*85} y="27" width="46" height="7" fill={C.gold} opacity={.4+.3*(i%3===0?1:0)}/>)}
<g opacity={question}>
<text x="160" y="195" fontSize="25" letterSpacing="5" fontWeight="bold">ФІЗИЧНИЙ АГРАРНИЙ РИНОК</text>
<g transform={`translate(${mix(50,0,e(t/.9))} 0)`}><text x="157" y="380" fontSize="99" fontWeight="900">ЧОМУ ЦІНИ</text><text x="157" y="497" fontSize="99" fontWeight="900">НА ЗЕРНО</text><text x="157" y="614" fontSize="99" fontWeight="900">РІЗНЯТЬСЯ?</text></g>
<Pixels word="SPOT" x={1150} y={220} size={22}/>
{Array.from({length:72},(_,i)=>{const row=Math.floor(i/12),col=i%12,p=e((t-.4)/2.9);const x=mix(1090+col*49,1190+col*40,p),y=mix(530+row*44,530+row*40+Math.sin(col*.7+t*.6)*36,p);return <g key={i} transform={`translate(${x} ${y}) rotate(-26)`}><rect x="-6" y="-16" width="12" height="32" rx="3" fill={i%5===0?C.gold:C.ink}/><path d="M0 -9 V10" stroke={C.lcd} strokeWidth="2"/></g>})}
<path d="M160 735 H1755" stroke={C.ink} opacity=".35"/><text x="160" y="805" fontSize="38">Одна культура. Різні умови. Різна ціна.</text>
</g>
<g opacity={factors}>
<text x="160" y="220" fontSize="68" fontWeight="bold">ЦІНА МАЄ КОНТЕКСТ</text>
{[{x:155,title:['БАЗИС','ПОСТАВКИ'],sub:['Де і на яких','умовах']},{x:710,title:['ЯКІСТЬ'],sub:['Що саме','постачається']},{x:1265,title:['ЛОГІСТИКА'],sub:['Як товар','дістанеться']}].map((card,i)=>{const active=e((t-(4.3+i*1.5))/.45);return <g key={i} transform={`translate(0 ${mix(100,0,e((t-4.15-i*.12)/.65))})`}><rect x={card.x} y="335" width="500" height="428" rx="12" fill={C.light} stroke={active>.5?C.ink:'#74805b'} strokeWidth={active>.5?6:2}/><rect x={card.x+24} y="360" width="452" height="12" fill={C.ink} opacity=".16"/><rect x={card.x+24} y="360" width={452*active} height="12" fill={C.gold}/><text x={card.x+32} y="432" fontSize="26" fontFamily="monospace">0{i+1} / УМОВИ РИНКУ</text>{card.title.map((s,j)=><text key={s} x={card.x+30} y={516+j*60} fontSize={i===2?53:59} fontWeight="bold">{s}</text>)}{card.sub.map((s,j)=><text key={s} x={card.x+32} y={675+j*39} fontSize="33">{s}</text>)}</g>})}
<text x="160" y="872" fontSize="33">Порівнювати ціну — означає розуміти умови.</text>
</g>
<g opacity={supply}>
<text x="160" y="230" fontSize="71" fontWeight="bold">ВІД ТОВАРУ ДО ПОСТАЧАННЯ</text>
<path d="M345 630 H1580" fill="none" stroke={C.ink} strokeWidth="12"/>
{Array.from({length:24},(_,i)=>{const x=350+((i*56+(t-9.35)*180)%1230);return <rect key={i} x={x} y={607+Math.sin(i)*3} width="14" height="42" fill={C.gold} stroke={C.ink} strokeWidth="2"/>})}
<g transform="translate(340 495)"><path d="M-60 30 Q-110 -90 -25 -140 Q-35 -30 -60 30 M-60 30 Q-15 -80 55 -105 Q65 -25 -60 30" fill={C.ink}/><path d="M-60 45 L15 -130" stroke={C.ink} strokeWidth="12"/></g>
<g transform="translate(900 500)"><path d="M-80 45 V-80 L0 -140 L80 -80 V45Z" fill={C.ink}/><path d="M-60 -60 H60 M-60 -25 H60 M-60 10 H60" stroke={C.lcd} strokeWidth="9"/><path d="M90 -100 H155 V50" fill="none" stroke={C.ink} strokeWidth="12"/></g>
<g transform="translate(1520 500)"><path d="M-100 -15 H110 L55 65 H-65Z M-40 -25 V-100 H50 V-25" fill={C.ink}/><path d="M80 -25 V-160 H155 M80 -160 L150 -85" fill="none" stroke={C.ink} strokeWidth="12"/></g>
{['ПОЛЕ','ЕЛЕВАТОР','ПОРТ'].map((s,i)=><text key={s} x={[310,920,1520][i]} y="745" textAnchor="middle" fontSize="46" fontWeight="bold">{s}</text>)}
<text x="160" y="876" fontSize="31">Товар · Якість · Місце · Умови · Виконання</text>
</g>
</svg>
<div style={{position:'absolute',inset:0,background:C.ink,color:C.light,opacity:close}}>
<svg width="1920" height="1080" style={{position:'absolute',inset:0}}><rect width="1920" height="1080" fill="url(#grid)"/><path d="M1120 0 L1010 1080 H1920 V0Z" fill="#2d3827"/><path d="M1120 0 L1010 1080" stroke={C.gold} strokeWidth="3"/>{Array.from({length:14},(_,i)=><rect key={i} x={1160+i*50} y="50" width="25" height="12" fill={C.gold} opacity=".35"/>)}</svg>
<div style={{position:'absolute',left:115,top:105,fontSize:25,letterSpacing:3,color:C.gold}}>БЕЗКОШТОВНО УКРАЇНСЬКОЮ</div>
<div style={{position:'absolute',left:108,top:225,fontSize:85,fontWeight:850,lineHeight:1.08,letterSpacing:-2,width:950}}>Практичний гайд<br/>по спотовому<br/>ринку</div>
<div style={{position:'absolute',left:115,top:545,fontSize:35,lineHeight:1.45,color:'#b9c29c'}}>Фізичний аграрний ринок.<br/>Базис. Якість. Логістика.</div>
<div style={{position:'absolute',left:115,top:695,display:'flex',gap:20}}>{['PDF','EPUB'].map(s=><div key={s} style={{fontSize:29,border:`2px solid ${C.gold}`,padding:'12px 26px',color:C.gold}}>{s}</div>)}</div>
<div style={{position:'absolute',left:115,top:838,fontSize:39,fontWeight:'bold'}}>Завантажуйте та читайте</div><div style={{position:'absolute',left:115,top:905,fontSize:30,color:C.gold}}>abvx.xyz · Розділ «Книги»</div>
<Img src={staticFile('cover.jpeg')} style={{position:'absolute',width:570,height:855,objectFit:'contain',right:120,top:115,boxShadow:'24px 26px 0 #0006',transform:`translateX(${80*(1-close)}px) rotate(-2deg)`}}/>
</div>
<svg width="1920" height="1080" style={{position:'absolute',inset:0,pointerEvents:'none'}}>{Array.from({length:12},(_,i)=>{const q=alpha(t,12.75+i*.025,13.12+i*.025);return <rect key={i} x={i*160} y="0" width="161" height="1080" fill={i%2?C.lcd:C.case} opacity={q}/>})}</svg>
<div style={{position:'absolute',left:115,bottom:28,fontSize:21,letterSpacing:3,color:t<13.2?C.light:C.gold}}>1D3X / MN7R · ПРАКТИЧНІ КНИГИ ПРО РИНОК</div>
</AbsoluteFill>}
export const Root=()=> <Composition id="SpotUK" component={Film} durationInFrames={720} fps={30} width={1920} height={1080}/>;
