import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {EffectComposer,RenderPass,EffectPass,PixelationEffect,BloomEffect} from 'postprocessing';
const W=1920,H=1080,DURATION=100;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const hash=n=>{let a=Math.sin(n*127.1+311.7)*43758.5453;return a-Math.floor(a)};
const xy=ll=>[(ll[0]+1.55)*75500,-(ll[1]-47.218)*111195];
const caption=document.getElementById('title'),eyebrow=document.getElementById('eyebrow'),small=document.getElementById('small'),photoLabel=document.getElementById('photo-label');
const mapCanvas=document.getElementById('map'),mg=mapCanvas.getContext('2d');mapCanvas.width=W;mapCanvas.height=H;
window.__hf??={};window.__hf.buildReady??={};window.__timelines??={};
const ready=(async()=>{
 const data=await(await fetch('assets/city.json')).json();const scene=new THREE.Scene();scene.background=new THREE.Color('#bed9e0');scene.fog=new THREE.Fog('#c7d7d5',80,330);
 const camera=new THREE.PerspectiveCamera(57,W/H,.08,1500);scene.add(camera);
 const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('view'),antialias:false,preserveDrawingBuffer:true});renderer.setSize(W,H);renderer.setPixelRatio(1);renderer.outputColorSpace=THREE.SRGBColorSpace;
 const composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,camera));const pix=new PixelationEffect(4);const bloom=new BloomEffect({intensity:.12,luminanceThreshold:1.1,luminanceSmoothing:.25,mipmapBlur:true});composer.addPass(new EffectPass(camera,bloom,pix));
 scene.add(new THREE.HemisphereLight('#e6f4ff','#897858',2.6));const sun=new THREE.DirectionalLight('#ffe4b6',2.3);sun.position.set(-50,80,-30);scene.add(sun);
 const ground=new THREE.Mesh(new THREE.PlaneGeometry(5000,5000),new THREE.MeshLambertMaterial({color:'#a7aa93'}));ground.rotation.x=-Math.PI/2;ground.position.y=-.06;scene.add(ground);
 function polygon(ps,y=0){const sh=new THREE.Shape(ps.map(p=>new THREE.Vector2(p[0],-p[1])));const g=new THREE.ShapeGeometry(sh);g.rotateX(-Math.PI/2);g.translate(0,y,0);return g;}
 function merged(list,mat){if(list.length){const m=new THREE.Mesh(mergeGeometries(list,false),mat);scene.add(m);return m}}
 const parkGs=[];for(const p of data.parks){if(p.length>3)try{parkGs.push(polygon(p,.012))}catch{}}
 merged(parkGs,new THREE.MeshLambertMaterial({color:'#8dba75'}));
 const roadGs=[],footGs=[];function ribbon(points,width,y){const v=[],indices=[];for(let i=0;i<points.length;i++){const a=points[Math.max(0,i-1)],b=points[Math.min(points.length-1,i+1)],dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz)||1;v.push(points[i][0]-dz/l*width/2,y,points[i][1]+dx/l*width/2,points[i][0]+dz/l*width/2,y,points[i][1]-dx/l*width/2);if(i<points.length-1){let n=i*2;indices.push(n,n+2,n+1,n+1,n+2,n+3)}}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.setIndex(indices);g.computeVertexNormals();return g;}
 for(const r of data.roads){const foot=['footway','pedestrian','path','steps','cycleway'].includes(r.kind);(foot?footGs:roadGs).push(ribbon(r.points,foot?4.5:10,foot?.028:.02));}
 merged(roadGs,new THREE.MeshLambertMaterial({color:'#7c8280',side:THREE.DoubleSide}));merged(footGs,new THREE.MeshLambertMaterial({color:'#d7ccb6',side:THREE.DoubleSide}));
 const allLines=data.fullRoute.map(l=>l.map(xy));merged(allLines.map(l=>ribbon(l,.18,.055)),new THREE.MeshBasicMaterial({color:'#53d52e',side:THREE.DoubleSide}));
 const groups=[[],[],[],[]],roofs=[];const facades=[];
 for(let k=0;k<4;k++){const c=document.createElement('canvas');c.width=128;c.height=256;let g=c.getContext('2d');g.fillStyle=['#d3c5a8','#e5ddc6','#cabca6','#e2c7ac'][k];g.fillRect(0,0,128,256);for(let y=7;y<255;y+=43){g.fillStyle='#839b9f';for(let x=12;x<128;x+=32){g.fillRect(x,y,14,24);g.fillStyle='#f3ebd5';g.fillRect(x+6,y,2,24);g.fillRect(x,y+12,14,2);g.fillStyle='#839b9f'}g.fillStyle='rgba(80,70,55,.15)';g.fillRect(0,y+33,128,2)}const tx=new THREE.CanvasTexture(c);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(.1,.1);tx.magFilter=THREE.NearestFilter;tx.minFilter=THREE.NearestMipmapNearestFilter;tx.colorSpace=THREE.SRGBColorSpace;facades.push(new THREE.MeshLambertMaterial({map:tx}));}
 let count=0;
 for(const b of data.buildings){const ps=b.points,cx=ps.reduce((s,p)=>s+p[0],0)/ps.length,cz=ps.reduce((s,p)=>s+p[1],0)/ps.length;let near=Math.min(...data.pois.map(p=>Math.hypot(cx-p.position[0],cz-p.position[1])));if(near>200||data.pois.some(p=>Math.hypot(cx-p.position[0],cz-p.position[1])<({cathedrale:62,chateau:75,musee:52,jardin:42,lu:36,gare:35}[p.id])))continue;
  try{const sh=new THREE.Shape(ps.map(p=>new THREE.Vector2(p[0],-p[1])));const geo=new THREE.ExtrudeGeometry(sh,{depth:b.height,bevelEnabled:false});geo.rotateX(-Math.PI/2);groups[b.id%4].push(geo);roofs.push(polygon(ps,b.height+.04));count++;}catch{}}
 groups.forEach((g,i)=>merged(g,facades[i]));merged(roofs,new THREE.MeshLambertMaterial({color:'#515f69'}));
 const leavesG=new THREE.IcosahedronGeometry(2.2,0),trunkG=new THREE.CylinderGeometry(.12,.22,3,5);const treeN=420;const leaves=new THREE.InstancedMesh(leavesG,new THREE.MeshLambertMaterial({color:'#679457'}),treeN);const trunks=new THREE.InstancedMesh(trunkG,new THREE.MeshLambertMaterial({color:'#756a50'}),treeN);const dummy=new THREE.Object3D();let ti=0;
 for(const p of data.pois){for(let n=0;n<70;n++){const a=hash(n+p.position[0])*6.28,r=18+hash(n*9+p.position[1])*95,x=p.position[0]+Math.cos(a)*r,z=p.position[1]+Math.sin(a)*r;let closeLine=Math.min(...allLines.flatMap(l=>l.map(q=>Math.hypot(q[0]-x,q[1]-z))));if(closeLine<5)continue;dummy.position.set(x,1.5,z);dummy.scale.set(1,1,1);dummy.updateMatrix();trunks.setMatrixAt(ti,dummy.matrix);dummy.position.y=4.1;dummy.scale.set(1.1,1.1+hash(n)*.6,1.1);dummy.updateMatrix();leaves.setMatrixAt(ti,dummy.matrix);ti++;if(ti>=treeN)break}if(ti>=treeN)break}
 leaves.count=trunks.count=ti;scene.add(leaves,trunks);
 let activeGroup=null,activeOrigin=[0,0];
 function mesh(g,color,x,y,z){let m=new THREE.Mesh(g,new THREE.MeshLambertMaterial({color,side:THREE.DoubleSide}));m.position.set(x-activeOrigin[0],y,z-activeOrigin[1]);(activeGroup||scene).add(m);return m}
 function gable(w,h,d=1){const sh=new THREE.Shape();sh.moveTo(-w/2,0);sh.lineTo(w/2,0);sh.lineTo(0,h);sh.closePath();return new THREE.ExtrudeGeometry(sh,{depth:d,bevelEnabled:false});}
 function arch(w,h){const sh=new THREE.Shape();sh.moveTo(-w/2,0);sh.lineTo(-w/2,h-w/2);sh.quadraticCurveTo(-w/2,h,0,h+w*.15);sh.quadraticCurveTo(w/2,h,w/2,h-w/2);sh.lineTo(w/2,0);sh.closePath();return new THREE.ShapeGeometry(sh);}
 for(const p of data.pois){const [x,z]=p.position;activeOrigin=[x,z];activeGroup=new THREE.Group();activeGroup.position.set(x,0,z);scene.add(activeGroup);
 if(p.id==='cathedrale'){
  mesh(new THREE.BoxGeometry(29,24,40),'#eadfc4',x,12,z-9);
  mesh(new THREE.BoxGeometry(31,23,8),'#eee5d1',x,11.5,z+14);
  for(const side of [-1,1]){mesh(new THREE.BoxGeometry(9,37,10),'#f1e6cd',x+side*11,18.5,z+14);mesh(new THREE.BoxGeometry(10,1,11),'#c4b89b',x+side*11,36,z+14);for(const off of [-2,2])mesh(arch(2.2,9),'#48545b',x+side*11+off,24,z+19.05);for(let y=8;y<34;y+=9)mesh(new THREE.BoxGeometry(9.5,.55,10.3),'#d0c3a8',x+side*11,y,z+14);}
  for(const off of [-9,0,9]){mesh(arch(6.1,10),'#b3a78d',x+off,0,z+19.12);mesh(arch(4.9,8.5),'#445052',x+off,0,z+19.18);}
  mesh(arch(6,11),'#748d94',x,10,z+18.2);mesh(gable(14,9,1),'#ded3bd',x,22.5,z+18);
  for(const off of [-15,-6,6,15])mesh(new THREE.BoxGeometry(.75,25,1.2),'#cfc3a9',x+off,12.5,z+19.8);
 }else if(p.id==='chateau'){
  mesh(new THREE.BoxGeometry(45,12,13),'#969a8d',x,6,z+9);
  for(const side of [-1,1]){mesh(new THREE.CylinderGeometry(7.3,7.3,18,18),'#aaa38e',x+side*23,9,z+7);mesh(new THREE.ConeGeometry(8.2,11,18),'#52616d',x+side*23,23,z+7);for(let a=0;a<9;a++){let an=a/9*6.283;mesh(new THREE.BoxGeometry(1.4,1.5,1.5),'#b9b19a',x+side*23+Math.cos(an)*6.6,18.4,z+7+Math.sin(an)*6.6);}}
  mesh(arch(7,9),'#354a4b',x,0,z+15.6);mesh(new THREE.BoxGeometry(28,24,15),'#e9dfc7',x,12,z-15);mesh(new THREE.ConeGeometry(20,9,4),'#5d6b73',x,28,z-15).rotation.y=Math.PI/4;
  for(let i=-2;i<=2;i++)for(let y=7;y<22;y+=7)mesh(new THREE.PlaneGeometry(1.6,3),'#597078',x+i*5,y,z-7.45);
 }else if(p.id==='lu'){
  mesh(new THREE.CylinderGeometry(4.3,5,31,16),'#c5a383',x,15.5,z);
  for(const y of [5,13,22,30])mesh(new THREE.CylinderGeometry(4.8,4.8,.55,16),'#efe0ba',x,y,z);
  mesh(new THREE.CylinderGeometry(5.3,4.3,7,16),'#82b6c0',x,34,z);mesh(new THREE.SphereGeometry(5.5,16,10,0,6.283,0,Math.PI/2),'#a9c5c5',x,37.5,z);mesh(new THREE.ConeGeometry(.4,6,8),'#b69749',x,45.5,z);
  const cv=document.createElement('canvas');cv.width=128;cv.height=256;const cg=cv.getContext('2d');cg.fillStyle='#294f57';cg.fillRect(0,0,128,256);cg.fillStyle='#f4df98';cg.font='bold 66px Georgia';cg.textAlign='center';cg.fillText('L',64,105);cg.fillText('U',64,185);let tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;let pl=new THREE.Mesh(new THREE.PlaneGeometry(3.4,7),new THREE.MeshBasicMaterial({map:tx}));pl.position.set(0,24,4.85);activeGroup.add(pl);
 }else if(p.id==='musee'){
  mesh(new THREE.BoxGeometry(50,16,18),'#e4d7ba',x,8,z);mesh(new THREE.BoxGeometry(52,1.2,20),'#eae3d1',x,16.7,z);
  for(let i=-4;i<=4;i++){mesh(new THREE.CylinderGeometry(.7,.85,12,8),'#f3e6c9',x+i*5.1,7,z+9.9);mesh(arch(2.5,5),'#5d7780',x+i*5.1,3,z+9.12);mesh(new THREE.BoxGeometry(1.7,.5,1.5),'#ded0b4',x+i*5.1,13,z+9.9);}
  mesh(gable(24,6,1),'#eee1c5',x,16.8,z+9);
  for(let i=0;i<5;i++)mesh(new THREE.BoxGeometry(28+i*2,.35,3),'#b8ae94',x,.15+i*.28,z+11.5+i*.6);
 }else if(p.id==='jardin'){
  mesh(new THREE.BoxGeometry(33,1,31),'#c5c7b0',x,.5,z);mesh(new THREE.BoxGeometry(30,11,27),'#99b8aa',x,6,z);
  let dome=mesh(new THREE.SphereGeometry(16,20,12,0,6.283,0,Math.PI/2),'#8ba99e',x,11,z);dome.scale.set(1,1,1.15);
  for(let a=0;a<9;a++){let an=a/9*3.1416;mesh(new THREE.TorusGeometry(16,.13,4,48,Math.PI),'#c9d6bd',x,11,z).rotation.y=an;}
  for(let i=-5;i<=5;i++)mesh(new THREE.BoxGeometry(.18,11,.2),'#d6dbc1',x+i*2.8,6,z+13.6);
  mesh(arch(4.5,8),'#365f5d',x,1,z+13.8);
 }else{
  mesh(new THREE.BoxGeometry(55,11,20),'#e8ddc5',x,5.5,z);mesh(new THREE.BoxGeometry(58,1.3,23),'#929f9d',x,11.4,z);
  for(let i=-5;i<=5;i++)mesh(new THREE.BoxGeometry(3.5,6,.25),'#68949a',x+i*4.5,5,z+10.2);
 }
 const an=nearestLine(p.eyePosition),eye=at(an.line,Math.max(0,an.at-4));activeGroup.rotation.y=Math.atan2(eye[0]-x,eye[1]-z);activeGroup=null;activeOrigin=[0,0];
 }
 const textures=await Promise.all(['jardin','musee','cathedrale','chateau','lu'].map(async id=>{let tx=await new THREE.TextureLoader().loadAsync('assets/'+id+'.png');tx.colorSpace=THREE.SRGBColorSpace;return[id,tx]}));const tex=Object.fromEntries(textures);
 const photoMat=new THREE.MeshBasicMaterial({map:tex.jardin,transparent:true,opacity:0,depthTest:false,depthWrite:false,fog:false});const photo=new THREE.Mesh(new THREE.PlaneGeometry(2,2),photoMat);photo.position.set(0,0,-.2);photo.renderOrder=999;camera.add(photo);
 function nearestLine(pos){let best={distance:1e9};allLines.forEach((l,idx)=>{let total=0;for(let i=1;i<l.length;i++){const a=l[i-1],b=l[i],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz),q=clamp(((pos[0]-a[0])*dx+(pos[1]-a[1])*dz)/(len*len||1)),x=a[0]+dx*q,z=a[1]+dz*q,dd=Math.hypot(x-pos[0],z-pos[1]);if(dd<best.distance)best={distance:dd,line:idx,at:total+q*len};total+=len}});return best}
 function at(line,s){let l=allLines[line];for(let i=1;i<l.length;i++){let a=l[i-1],b=l[i],d=Math.hypot(b[0]-a[0],b[1]-a[1]);if(s<=d)return[a[0]+(b[0]-a[0])*clamp(s/d),a[1]+(b[1]-a[1])*clamp(s/d)];s-=d}return l[l.length-1]}
 const stops=data.pois.map(p=>({...p,anchor:nearestLine(p.eyePosition)}));
 const startTimes=[0,16,31,46,61,76];
 const titles=['De la gare, suivez le vert.','Un jardin en plein cœur de ville.','Neuf siècles de création.','La pierre, la lumière, le silence.','Six siècles derrière les remparts.','LU : des biscuits à la culture.'];
 const subtitles=['Gare de Nantes · départ','Jardin des plantes','Musée d’arts de Nantes','Cathédrale Saint-Pierre-et-Saint-Paul','Château des ducs de Bretagne','Tour LU · Le Lieu Unique'];
 const bounds=data.fullRoute.flat().reduce((b,p)=>[Math.min(b[0],p[0]),Math.min(b[1],p[1]),Math.max(b[2],p[0]),Math.max(b[3],p[1])],[100,100,-100,-100]);
 function drawMap(t,alpha){mapCanvas.style.opacity=alpha;if(alpha<=0)return;const g=mg;g.fillStyle='#102e32';g.fillRect(0,0,W,H);const w=(bounds[2]-bounds[0])*75500,h=(bounds[3]-bounds[1])*111195,scale=Math.min(1060/w,800/h),mx=1180,my=525;const project=ll=>[mx+((ll[0]-(bounds[0]+bounds[2])/2)*75500)*scale,my-((ll[1]-(bounds[1]+bounds[3])/2)*111195)*scale];
  g.strokeStyle='#1c4446';g.lineWidth=1;for(let x=650;x<W;x+=80){g.beginPath();g.moveTo(x,100);g.lineTo(x,H-100);g.stroke()}for(let y=100;y<H;y+=80){g.beginPath();g.moveTo(650,y);g.lineTo(W,y);g.stroke()}
  g.save();g.beginPath();g.rect(650,95,1160,855);g.clip();
  const projectXY=p=>project([p[0]/75500-1.55,47.218-p[1]/111195]);
  g.fillStyle='#25565d';for(const l of data.waters){if(l.length<3)continue;g.beginPath();l.forEach((p,i)=>{const q=projectXY(p);i?g.lineTo(...q):g.moveTo(...q)});g.closePath();g.fill()}
  g.strokeStyle='#2b4c4a';g.lineWidth=.8;for(const r of data.roads){g.beginPath();r.points.forEach((p,i)=>{const q=projectXY(p);i?g.lineTo(...q):g.moveTo(...q)});g.stroke()}g.restore();
  g.fillStyle='#7399a0';g.font='italic 23px Georgia';g.fillText('La Loire',1135,730);
  g.strokeStyle='#b5eb70';g.lineWidth=5;g.lineCap='round';for(let l of data.fullRoute){g.beginPath();l.forEach((p,i)=>{const q=project(p);i?g.lineTo(...q):g.moveTo(...q)});g.stroke()}
  const labelOffsets=[[55,35],[36,-28],[-24,-55],[-66,-15],[-45,34],[30,65]];
  for(let i=0;i<stops.length;i++){let q=project(stops[i].ll),o=labelOffsets[i],lx=q[0]+o[0],ly=q[1]+o[1];g.strokeStyle='#d5edc5';g.lineWidth=1;g.beginPath();g.moveTo(...q);g.lineTo(lx,ly);g.stroke();g.fillStyle='#e9f3d5';g.beginPath();g.arc(q[0],q[1],4,0,Math.PI*2);g.fill();g.fillStyle='#e9f3d5';g.beginPath();g.arc(lx,ly,14,0,Math.PI*2);g.fill();g.fillStyle='#173b3d';g.font='bold 18px Arial';g.textAlign='center';g.fillText(String(i+1),lx,ly+6);g.textAlign='left'}
  g.fillStyle='#e7f0df';g.font='bold 28px Arial';g.fillText('LE TRACÉ COMPLET',115,215);g.font='72px Georgia';g.fillText('Une ligne.',110,320);g.fillText('Toute une ville.',110,406);g.font='25px Arial';g.fillStyle='#b8d4c5';g.fillText('Tracé officiel · carte de synthèse',115,472);g.fillText('Les scènes du film : étapes 1 à 6',115,515);g.font='24px Arial';subtitles.forEach((s,i)=>g.fillText((i+1)+'. '+s,115,590+i*44));g.fillStyle='#9db7a9';g.font='18px Arial';g.fillText('Tracé : Le Voyage à Nantes · carte de synthèse',115,987);
 }
 function draw(t){t=clamp(t,0,DURATION);let idx=startTimes.findLastIndex(s=>t>=s);idx=Math.max(0,idx);let p=stops[idx],local=t-startTimes[idx],walkTime=Math.min(local,15);let pos=at(p.anchor.line,Math.max(0,p.anchor.at-14+walkTime*1.35));let ahead=at(p.anchor.line,Math.max(0,p.anchor.at-14+walkTime*1.35+8));let focus=idx? smooth((local-5)/2.2)*(1-smooth((local-12.1)/2.3)):0;
  camera.position.set(pos[0],1.68+Math.sin(walkTime*11.3)*.022*(1-focus),pos[1]);let target=new THREE.Vector3(ahead[0],1.7,ahead[1]);target.lerp(new THREE.Vector3(p.position[0],({lu:21,cathedrale:18,jardin:10}[p.id]||10),p.position[1]),focus);camera.lookAt(target);camera.fov=57-9*focus;camera.updateProjectionMatrix();
  let a=idx? smooth((local-7.5)/.8)*(1-smooth((local-11.2)/.8)):0;photoMat.opacity=a;photo.visible=a>0;photoMat.map=tex[p.id]||tex.jardin;let planeH=2*Math.tan(THREE.MathUtils.degToRad(camera.fov/2))*.2;photo.scale.set(planeH*W/H*.52*(1+local*.001),planeH*.52*(1+local*.001),1);pix.granularity=4*(1-smooth((local-8.2)/.65)*(1-smooth((local-10.4)/.7)));photoLabel.style.opacity=a;
  caption.textContent=t>=91?'La balade continue.':titles[idx];eyebrow.textContent=t>=91?'NANTES · LA LIGNE VERTE':subtitles[idx];small.textContent='Promenade illustrée · étapes sélectionnées';
  if(t>=91){photoMat.opacity=0;photo.visible=false;pix.granularity=4;camera.position.y=4+(t-91)*1.5;camera.lookAt(p.position[0],8,p.position[1]);}
  composer.render(0);let ma=smooth((t-8.3)/.7)*(1-smooth((t-14.6)/.7));if(t>=96)ma=smooth(t-96);drawMap(t,ma);document.getElementById('hud').style.opacity=1-ma;window.walkState={t,stop:p.id,photo:a,pixel:pix.granularity,map:ma,eyeHeight:camera.position.y,buildings:count};
 }
 window.addEventListener('hf-seek',e=>draw(e.detail.time));window.greenWalk={draw,duration:DURATION,stops:stops.map(p=>({id:p.id,anchor:p.anchor}))};draw(0);

 return {buildings:count,stops:stops.length,postprocessing:'6.39.5',three:THREE.REVISION};
})();window.__hf.buildReady.scene=ready;
