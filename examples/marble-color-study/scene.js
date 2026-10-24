import * as T from './assets/three.module.js';
const W=1920,H=1080,canvas=document.querySelector('#film'),ctx=canvas.getContext('2d');
const plate=new Image();plate.src='./assets/forest-plate.png';await plate.decode();
const gl=new T.WebGLRenderer({alpha:true,antialias:true,preserveDrawingBuffer:true});gl.setSize(W,H);gl.setPixelRatio(1);gl.setClearColor(0,0);gl.outputColorSpace=T.SRGBColorSpace;gl.toneMapping=T.ACESFilmicToneMapping;gl.toneMappingExposure=1.15;
const scene=new T.Scene(),camera=new T.OrthographicCamera(-9.6,9.6,5.4,-5.4,.1,100);camera.position.set(0,0,30);
scene.add(new T.HemisphereLight(0xa8d7ee,0x222520,.9));const moon=new T.DirectionalLight(0xa0d9ff,1.4);moon.position.set(-3,8,-4);scene.add(moon);const fill=new T.DirectionalLight(0xffbc77,1.6);fill.position.set(2,3,8);scene.add(fill);
const cloth=new T.MeshStandardMaterial({color:0x71645b,roughness:.97}),dark=new T.MeshStandardMaterial({color:0x111b22,roughness:.88}),leather=new T.MeshStandardMaterial({color:0x382d24,roughness:.85}),skin=new T.MeshStandardMaterial({color:0xb19982,roughness:1}),metal=new T.MeshStandardMaterial({color:0x343f43,metalness:.7,roughness:.45});
const hero=new T.Group();scene.add(hero);hero.rotation.y=Math.PI/2;
function ellipsoid(parent,r,x,y,z,sx,sy,sz,material){let m=new T.Mesh(new T.SphereGeometry(r,24,16),material);m.position.set(x,y,z);m.scale.set(sx,sy,sz);parent.add(m);return m;}
function segment(parent,a,b,r1,r2,mat){let m=new T.Mesh(new T.CylinderGeometry(r1,r2,1,16),mat);parent.add(m);place(m,a,b);return m;}
function place(m,a,b){m.position.copy(a).add(b).multiplyScalar(.5);m.scale.y=a.distanceTo(b);m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),b.clone().sub(a).normalize());}
const body=new T.Group();hero.add(body);
const coat=new T.Mesh(new T.LatheGeometry([new T.Vector2(.29,.82),new T.Vector2(.27,1.15),new T.Vector2(.22,1.42),new T.Vector2(.31,1.68),new T.Vector2(.23,1.8)],32),cloth);coat.scale.z=.67;body.add(coat);
ellipsoid(body,.185,0,1.94,0,1.05,1.1,1,cloth);ellipsoid(body,.132,0,1.94,.11,.76,.94,.40,dark);ellipsoid(body,.06,0,1.90,.15,.7,.75,.38,skin);
const pack=ellipsoid(body,.26,0,1.45,-.24,1,.98,.45,leather);segment(body,new T.Vector3(-.2,1.69,-.1),new T.Vector3(-.2,1.18,.08),.026,.026,leather);segment(body,new T.Vector3(.2,1.69,-.1),new T.Vector3(.2,1.18,.08),.026,.026,leather);
const legs=[];for(const side of [-1,1]){const up=segment(hero,new T.Vector3(),new T.Vector3(0,1,0),.096,.078,dark),low=segment(hero,new T.Vector3(),new T.Vector3(0,1,0),.077,.059,dark),boot=ellipsoid(hero,.13,0,0,0,.66,.6,1.35,leather);legs.push({side,up,low,boot});}
const arms=[];for(const side of [-1,1]){const up=segment(body,new T.Vector3(),new T.Vector3(0,1,0),.095,.07,cloth),low=segment(body,new T.Vector3(),new T.Vector3(0,1,0),.071,.05,cloth),hand=ellipsoid(body,.062,0,0,0,1,1.2,1,leather);arms.push({side,up,low,hand});}
const lamp=new T.Group();hero.add(lamp);const glowMat=new T.MeshStandardMaterial({color:0xffc16f,emissive:0xff830c,emissiveIntensity:2.8,roughness:.35});ellipsoid(lamp,.068,0,0,0,.8,1.35,.8,glowMat);for(const z of [-.054,.054])for(const x of [-.054,.054])segment(lamp,new T.Vector3(x,-.1,z),new T.Vector3(x,.1,z),.008,.008,metal);const lampLight=new T.PointLight(0xffa842,2.4,2);lamp.add(lampLight);
// Locked-camera crop and hand-authored foreground holdout belong to this shot only.
const crop=[420,100,1320,742.5];
const foreground=new Path2D();foreground.moveTo(1120,0);foreground.lineTo(1238,0);foreground.bezierCurveTo(1207,220,1197,450,1220,610);foreground.lineTo(1272,676);foreground.lineTo(1120,683);foreground.lineTo(1161,614);foreground.bezierCurveTo(1175,430,1171,230,1120,0);foreground.closePath();
const grades=[],holds=[];
for(let mood=0;mood<3;mood++){
 const c=document.createElement('canvas');c.width=plate.width;c.height=plate.height;const cx=c.getContext('2d');cx.drawImage(plate,0,0);const im=cx.getImageData(0,0,c.width,c.height),d=im.data;
 for(let i=0;i<d.length;i+=4){let r=Math.pow(.018+.982*d[i]/255,.70),g=Math.pow(.018+.982*d[i+1]/255,.70),b=Math.pow(.018+.982*d[i+2]/255,.70);const lum=.2126*r+.7152*g+.0722*b;
 let rr,gg,bb;if(mood===0){rr=r*.72;gg=g*.98;bb=b*1.20;}else if(mood===1){rr=lum*1.64+r*.08;gg=lum*1.23;bb=lum*.48+b*.06;}else{rr=lum*1.26;gg=lum*.64+g*.12;bb=lum*.55+b*.24;}
 d[i]=Math.min(255,(rr+.013)*255);d[i+1]=Math.min(255,(gg+.017)*255);d[i+2]=Math.min(255,(bb+.022)*255);}
 cx.putImageData(im,0,0);grades.push(c);const h=document.createElement('canvas');h.width=c.width;h.height=c.height;const hx=h.getContext('2d');hx.clip(foreground);hx.drawImage(c,0,0);holds.push(h);
}
hero.scale.setScalar(1.42);
let thumbnailMode=false;
let playing=true,base=performance.now(),offset=0,muted=true,bot=true,now=0;
function smooth(a,b,x){x=Math.max(0,Math.min(1,(x-a)/(b-a)));return x*x*(3-2*x);}
function frame(t){now=t;const walkTime=Math.max(0,Math.min(t-3,25)),phase=walkTime*2*Math.PI/1.2,bob=.014*Math.cos(phase*2),stop=1-smooth(3,3.5,t)+smooth(27.5,28,t),warm=smooth(13,15,t),red=smooth(25,27.2,t);
const travel=.40*Math.min(walkTime,10)+.36*Math.max(0,Math.min(walkTime-10,12))+.12*Math.max(0,walkTime-22);
hero.position.set(-5.45+travel-.16*smooth(30.8,31.3,t),-3.48,0);body.position.y=bob*(1-stop);body.rotation.z=.017*Math.sin(phase)*(1-stop);body.rotation.x=.025;body.rotation.y=-.68*smooth(28,29.3,t);
for(const l of legs){const p=(walkTime/1.2+(l.side===1?.5:0))%1;let z,y;if(p<.6){z=.269-p/.6*.538;y=.065;}else{const v=(p-.6)/.4;z=-.269+v*.538;y=.065+.12*Math.sin(Math.PI*v);}z*=1-stop;y=.065+(y-.065)*(1-stop);const hip=new T.Vector3(l.side*.105,1.08+bob*(1-stop),0),foot=new T.Vector3(l.side*.105,y,z),d=hip.distanceTo(foot),mid=hip.clone().add(foot).multiplyScalar(.5),bend=Math.sqrt(Math.max(0,.55*.55-d*d/4));mid.z+=bend;place(l.up,hip,mid);place(l.low,mid,foot);l.boot.position.copy(foot).add(new T.Vector3(0,-.015,.065));}
for(const a of arms){const sh=new T.Vector3(a.side*.26,1.66,0),el=new T.Vector3(a.side*.32,1.36,.10+.09*Math.sin(phase+a.side*Math.PI/2)*(1-stop)),hand=new T.Vector3(a.side*.29,1.1,.14+.11*Math.sin(phase+a.side*Math.PI/2)*(1-stop));if(a.side===-1){const lift=smooth(27.7,29.2,t);hand.y+=.48*lift;hand.z+=.16*lift;el.y+=.13*lift;}place(a.up,sh,el);place(a.low,el,hand);a.hand.position.copy(hand);if(a.side===-1)lamp.position.copy(hand).add(new T.Vector3(0,-.15,0));}
const cold=new T.Color(0x92c4ee),amber=new T.Color(0xffce8c),danger=new T.Color(0xff795e);fill.color.copy(cold).lerp(amber,warm).lerp(danger,red);fill.intensity=.55+warm*.95+red*.12;moon.intensity=1.6;lampLight.intensity=2.1+warm*.6;gl.render(scene,camera);
function layer(image,alpha=1){ctx.globalAlpha=alpha;ctx.drawImage(image,...crop,0,0,W,H);ctx.globalAlpha=1;}
ctx.clearRect(0,0,W,H);layer(grades[0]);layer(grades[1],warm);layer(grades[2],red);
const footX=960+hero.position.x*100,footY=880;
// Ground contact and light pool are authored approximations, not exported depth.
ctx.save();ctx.translate(footX,footY);ctx.scale(1,.23);let shadow=ctx.createRadialGradient(0,0,2,0,0,90);shadow.addColorStop(0,'rgba(0,0,0,.6)');shadow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=shadow;ctx.fillRect(-110,-100,220,200);ctx.restore();
ctx.drawImage(gl.domElement,0,0); // The new route is in front of these middle-distance trees; do not reuse a rear-route holdout.
ctx.save();ctx.globalCompositeOperation='screen';let spill=ctx.createRadialGradient(footX+20,footY-95,5,footX+20,footY-95,170);spill.addColorStop(0,'rgba(249,171,76,.12)');spill.addColorStop(1,'rgba(249,171,76,0)');ctx.fillStyle=spill;ctx.fillRect(footX-180,footY-280,400,400);ctx.restore();
// Gentle drifting low mist; no flashing/strobe effect.
for(let k=0;k<3;k++){const x=350+k*610+Math.sin(t*.14+k)*80,y=650+k*25;const fog=ctx.createRadialGradient(x,y,20,x,y,520);const col=red>.5?'144,105,115':warm>.6?'153,160,146':'115,174,207';fog.addColorStop(0,`rgba(${col},.07)`);fog.addColorStop(1,`rgba(${col},0)`);ctx.fillStyle=fog;ctx.fillRect(x-540,y-520,1080,1040);}
// A local editorial push/crop is a 2D finish, not a new world camera export.
const closing=smooth(36,37.2,t);if(closing>0){ctx.fillStyle=`rgba(6,10,14,${.57*closing})`;ctx.fillRect(0,0,W,H);}
const opening=1-smooth(2.3,3,t),middle=smooth(3,3.7,t)*(1-smooth(35.5,36.5,t));
ctx.save();ctx.shadowColor='rgba(0,0,0,.65)';ctx.shadowBlur=12;ctx.fillStyle='#f2eee2';
if(opening>0){ctx.globalAlpha=opening*smooth(0,.6,t);ctx.font='600 74px Arial';ctx.fillText('THE SAME FOREST',106,168);ctx.font='400 30px Arial';ctx.fillStyle='#cfdae0';ctx.fillText('A story told with color',110,222);}
ctx.globalAlpha=thumbnailMode?0:middle;ctx.fillStyle='#f2eee2';ctx.font='600 37px Arial';ctx.fillText(t<13.8?'ALONE':t<25.9?'ALMOST HOME':'SOMETHING IS WRONG',88,105);ctx.font='400 25px Arial';ctx.fillStyle='#d7d9d4';ctx.fillText(t<13.8?'A path without a promise.':t<25.9?'The same light starts to feel like shelter.':'The way home no longer feels safe.',89,148);
if(closing>0){ctx.globalAlpha=closing*(1-smooth(40.8,42,t));ctx.fillStyle='#f2eee2';ctx.font='600 70px Arial';ctx.fillText('ONE FOREST.',106,425);ctx.fillText('THREE FEELINGS.',106,510);ctx.fillStyle='#d7d9d4';ctx.font='400 28px Arial';ctx.fillText('An experiment in light, color & sound.',110,569);ctx.font='400 22px Arial';ctx.fillText('An independently animated character study',110,624);}
ctx.restore();
const fade=smooth(0,.45,t)*(1-smooth(40.8,42,t));if(fade<1){ctx.fillStyle=`rgba(3,6,9,${1-fade})`;ctx.fillRect(0,0,W,H);}

}
window.renderThumbnail=()=>{
 thumbnailMode=true;const captures=[];for(const t of [9,20,31]){frame(t);const c=document.createElement('canvas');c.width=W;c.height=H;c.getContext('2d').drawImage(canvas,0,0);captures.push(c);}
 thumbnailMode=false;ctx.clearRect(0,0,W,H);for(let i=0;i<3;i++){ctx.save();ctx.beginPath();ctx.rect(i*640,0,640,H);ctx.clip();ctx.drawImage(captures[i],-350+i*640,0,W,H);ctx.restore();}
 const shade=ctx.createLinearGradient(0,0,0,800);shade.addColorStop(0,'rgba(2,6,9,.9)');shade.addColorStop(.65,'rgba(2,6,9,.3)');shade.addColorStop(1,'rgba(2,6,9,0)');ctx.fillStyle=shade;ctx.fillRect(0,0,W,H);ctx.shadowColor='rgba(0,0,0,.8)';ctx.shadowBlur=15;ctx.fillStyle='#f8f3e8';ctx.font='900 144px Arial';ctx.fillText('SAME FOREST.',84,191);ctx.fillStyle='#f0b75d';ctx.fillText('NEW FEELING.',84,348);ctx.font='600 38px Arial';ctx.fillStyle='#e1e7e4';ctx.fillText('LIGHT  ×  COLOR  ×  SOUND',93,420);ctx.shadowBlur=0;
};
window.renderAt=frame;window.FramewrightCapture={state:()=>({ready:true,t:now,playing,muted,bot}),play(){if(!playing){base=performance.now();playing=true;}},pause(){offset=now;playing=false;},seek(t){offset=t;base=performance.now();frame(t);},mute(v){muted=v;},setBot(v){bot=v;}};
function tick(){let t=playing?offset+(performance.now()-base)/1000:offset;if(t>=42){t=42;offset=42;playing=false;}if(playing||t===42)frame(t);requestAnimationFrame(tick);}document.querySelector('#replay').onclick=()=>{offset=0;base=performance.now();playing=true;};tick();
