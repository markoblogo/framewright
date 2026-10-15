import * as THREE from './three.module.js';
await document.fonts.ready;
const canvas=document.getElementById('market-canvas');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(1920,1080);renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.25;
const scene=new THREE.Scene();scene.background=new THREE.Color('#0b2025');scene.fog=new THREE.Fog('#0b2025',26,55);
const camera=new THREE.PerspectiveCamera(37,1920/1080,.1,100);scene.add(new THREE.HemisphereLight('#d8ebdd','#18292c',2.1));
const sun=new THREE.DirectionalLight('#ffe4b1',4.2);sun.position.set(-4,13,8);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-15;sun.shadow.camera.right=15;sun.shadow.camera.top=15;sun.shadow.camera.bottom=-15;sun.shadow.bias=-.0005;scene.add(sun);
const fill=new THREE.DirectionalLight('#6ac5c7',1.8);fill.position.set(8,6,-9);scene.add(fill);
const world=new THREE.Group();scene.add(world);
const mat=(c,roughness=.6,metalness=.1)=>new THREE.MeshStandardMaterial({color:c,roughness,metalness});
const green=mat('#335b56'),silver=mat('#a4b7af',.4,.48),cream=mat('#ebdfbd'),gold=mat('#d6b366',.38,.3),dark=mat('#122c32'),rust=mat('#a45b44'),rubber=mat('#192528'),teal=mat('#51b3ab');
function box(parent,w,h,d,m,x=0,y=0,z=0){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
function cylinder(parent,r1,r2,h,m,x,y,z,segments=24){const o=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,segments),m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
const floor=new THREE.Mesh(new THREE.PlaneGeometry(150,150),mat('#0c252a',.85,0));floor.rotation.x=-Math.PI/2;floor.position.y=-.22;floor.receiveShadow=true;scene.add(floor);
box(world,18,.22,12,mat('#18383b'),0,-.1,0);
for(let x=-8;x<=8;x+=1){const line=new THREE.Mesh(new THREE.BoxGeometry(.012,.005,11),mat('#315152'));line.position.set(x,.016,0);world.add(line);}
for(let z=-5;z<=5;z+=1){const line=new THREE.Mesh(new THREE.BoxGeometry(17,.005,.012),mat('#315152'));line.position.set(0,.016,z);world.add(line);}
// Commodity handling: bins, hopper, conveyor, warehouse.
const silos=new THREE.Group();silos.position.set(-5.7,0,-1.3);world.add(silos);
for(let i=0;i<3;i++){cylinder(silos,.68,.68,2.3,silver,(i-1)*1.45,1.45,0);cylinder(silos,0,.72,.48,green,(i-1)*1.45,2.84,0);box(silos,.08,2.9,.08,cream,(i-1)*1.45-.45,1.45,.56);for(let j=0;j<6;j++){const ring=new THREE.Mesh(new THREE.TorusGeometry(.685,.017,6,32),green);ring.rotation.x=Math.PI/2;ring.position.set((i-1)*1.45,.55+j*.37,0);silos.add(ring);}}
box(silos,4.5,.12,.35,cream,0,3.02,.25);
box(world,2.2,1.1,1.5,green,-6,.6,-3.65);const roof=box(world,2.5,.12,1.8,gold,-6,1.27,-3.65);roof.rotation.z=.08;
// Conveyor points toward the loading position.
const conveyor=box(world,2.4,.22,.5,dark,-4.8,1.55,.6);conveyor.rotation.y=-.58;conveyor.rotation.z=-.2;
for(let j=0;j<8;j++){const roller=box(world,.055,.06,.46,gold,-5.8+j*.28,1.7-j*.04,.02+j*.16);roller.rotation.y=-.58;}
const road=new THREE.CatmullRomCurve3([new THREE.Vector3(-4.2,.08,2),new THREE.Vector3(-2,.08,3.1),new THREE.Vector3(1,.08,2.8),new THREE.Vector3(3.5,.08,.6),new THREE.Vector3(3.7,.08,-2.2)]);
const route=new THREE.Mesh(new THREE.TubeGeometry(road,80,.052,8,false),new THREE.MeshStandardMaterial({color:'#dcc581',emissive:'#bf963d',emissiveIntensity:.55}));world.add(route);
for(let i=0;i<9;i++){const p=road.getPoint(i/8);cylinder(world,.1,.1,.03,cream,p.x,.1,p.z,16);}
// The truck is a moving model, not a flat picture.
const truck=new THREE.Group();world.add(truck);box(truck,2.5,.17,.95,dark,0,.42,0);box(truck,.72,.65,1.0,cream,.92,.87,0);box(truck,.53,.34,1.04,teal,1.01,1.02,0);box(truck,.78,.18,.85,cream,1.05,1.19,0);box(truck,.07,.16,.16,gold,1.32,.7,.33);box(truck,.07,.16,.16,gold,1.32,.7,-.33);
const wheels=[];for(const x of [-.88,.8])for(const z of [-.57,.57]){const w=cylinder(truck,.26,.26,.17,rubber,x,.36,z,20);w.rotation.x=Math.PI/2;wheels.push(w);const hub=cylinder(truck,.12,.12,.18,silver,x,.36,z,12);hub.rotation.x=Math.PI/2;}
const cargo=box(truck,1.5,.53,.9,gold,-.34,.8,0);const grainTop=box(truck,1.35,.09,.78,mat('#e6c46c'),-.34,1.105,0);
for(let i=0;i<9;i++)box(truck,.022,.49,.925,rust,-1.02+i*.17,.81,0);
// Dock, water, cargo ship and crane.
box(world,4.5,.1,6.8,mat('#24585d',.3,.3),5.7,.01,-1.5);box(world,1.2,.38,7,dark,3.65,.23,-1.5);
for(let i=0;i<13;i++)box(world,.45,.011,.025,mat('#7ba4a1'),4.6+(i%3)*1.1,.08,-4.2+Math.floor(i/3)*1.35);
const ship=new THREE.Group();ship.position.set(6.1,.05,-1.55);world.add(ship);const hull=box(ship,1.85,.52,5.1,dark,0,.42,0);const bow=new THREE.Mesh(new THREE.ConeGeometry(.93,1.25,4),rust);bow.rotation.x=Math.PI/2;bow.rotation.z=Math.PI/4;bow.position.set(0,.45,-3.1);ship.add(bow);box(ship,1.65,.12,4.8,rust,0,.74,0);box(ship,1.3,.95,.9,cream,0,1.18,1.55);box(ship,1.45,.3,.98,teal,0,1.62,1.55);
for(let i=0;i<6;i++){const c=box(ship,.72,.52,1.05,[gold,green,rust][i%3],(i%2-.5)*.8,1.02,-1.7+Math.floor(i/2)*1.15);for(let j=0;j<4;j++)box(ship,.018,.49,1.07,dark,c.position.x-.28+j*.18,1.02,c.position.z);}
const crane=new THREE.Group();crane.position.set(3.8,0,-2.4);world.add(crane);box(crane,.18,4,.18,gold,0,2,0);box(crane,.18,4,.18,gold,.9,2,0);box(crane,3.9,.18,.2,gold,1.5,4.04,0);box(crane,.03,2,.03,cream,2.65,3,0);box(crane,.5,.09,.4,rust,2.65,1.99,0);
// Label textures stay local and deterministic.
function textTexture(text,sub=''){const c=document.createElement('canvas');c.width=1024;c.height=512;const x=c.getContext('2d');x.fillStyle='#e9dfbf';x.fillRect(0,0,1024,512);x.fillStyle='#112f35';x.font='bold 94px Display';x.textAlign='center';x.fillText(text,512,240);x.fillStyle='#84693e';x.font='44px Display';x.fillText(sub,512,345);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;}
function ticket(text,sub,x,y,z){const g=new THREE.Group();const m=box(g,2.65,.09,1.3,cream);const face=new THREE.Mesh(new THREE.PlaneGeometry(2.65,1.3),new THREE.MeshBasicMaterial({map:textTexture(text,sub)}));face.rotation.x=-Math.PI/2;face.position.y=.051;g.add(face);g.position.set(x,y,z);g.rotation.set(.08,-.15,.02);world.add(g);return g;}
const tickets=[ticket('LOCAL QUOTES','NOISY SIGNALS',-4.8,4.1,1.2),ticket('DELIVERY','TERMS & ROUTES',-.25,3.7,-2.7),ticket('LIQUIDITY','MARKET DEPTH',4.8,3.9,.2)];const origins=tickets.map(t=>t.position.clone());
const benchmark=new THREE.Group();benchmark.position.set(.2,.2,-.5);world.add(benchmark);const beaconMaterial=new THREE.MeshStandardMaterial({color:'#77bdb0',emissive:'#46bca8',emissiveIntensity:.9,metalness:.5,roughness:.26});box(benchmark,2.1,.3,2.1,dark,0,.15,0);for(let i=0;i<3;i++){const o=box(benchmark,1.5-i*.28,.28,1.5-i*.28,beaconMaterial,0,.55+i*.45,0);o.rotation.y=Math.PI/4;}
const benchmarkLabel=ticket('BENCHMARK','SHARED REFERENCE',.2,2.1,-.5);benchmarkLabel.visible=false;
const particles=[];for(let i=0;i<22;i++){const g=new THREE.Mesh(new THREE.SphereGeometry(.065,6,4),gold);g.scale.set(1,.7,1.35);world.add(g);particles.push(g);}
const cover=await new THREE.TextureLoader().loadAsync('assets/cover.png');cover.colorSpace=THREE.SRGBColorSpace;cover.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
const book=new THREE.Group();scene.add(book);box(book,3.0,4.5,.38,cream,0,0,0);box(book,3.08,4.58,.055,dark,0,0,-.215);box(book,3.08,4.58,.055,dark,0,0,.215);box(book,.10,4.58,.50,dark,-1.53,0,0);
const coverPlane=new THREE.Mesh(new THREE.PlaneGeometry(3.075,4.575),new THREE.MeshStandardMaterial({map:cover,roughness:.7}));coverPlane.position.z=.247;book.add(coverPlane);
for(let i=0;i<20;i++)box(book,.025,.01,.35,mat('#c4baa0'),1.505,-2.12+i*.222,0);
const smooth=(a,b,t)=>{const p=THREE.MathUtils.clamp((t-a)/(b-a),0,1);return p*p*(3-2*p);};const lerp=THREE.MathUtils.lerp;
function renderAt(t){
 const travel=smooth(5.6,10.5,t),p=road.getPoint(travel),tangent=road.getTangent(travel);truck.position.copy(p);truck.rotation.y=-Math.atan2(tangent.z,tangent.x);for(const w of wheels)w.rotation.y=travel*24;
 grainTop.visible=t>4.1;grainTop.scale.y=.15+.85*smooth(4,5.6,t);
 for(let i=0;i<particles.length;i++){const f=((t-3.5)*1.3+i/particles.length)%1;const live=t>=3.5&&t<=5.6;particles[i].visible=live;if(live)particles[i].position.set(-4.6+f*.42+(i%3)*.035,1.85-f*.65,.85+f*.8);}
 const merge=smooth(11.5,14.1,t);tickets.forEach((q,i)=>{q.position.lerpVectors(origins[i],new THREE.Vector3(.2+(i-1)*.32,1.5+i*.1,-.5),merge);q.rotation.y=-.15+merge*.9;q.scale.setScalar((1-.94*merge)*(t<11?1-smooth(2.8,3.2,t):smooth(11.3,11.6,t)));q.visible=t<3.2||(t>11.3&&t<14.2);});benchmark.scale.setScalar(Math.max(.001,smooth(12,14.4,t)));benchmark.rotation.y=t*.08;benchmarkLabel.visible=t>13.2&&t<15;benchmarkLabel.scale.setScalar(smooth(13.2,14,t));
 const exit=smooth(14.2,17,t);world.position.x=-exit*12;world.scale.setScalar(1-exit*.25);world.visible=t<17;
 const reveal=smooth(14.5,16.8,t);book.visible=t>14.5;book.position.set(3.05,-1.3+4.1*reveal,.2);book.scale.setScalar(.4+1.05*reveal);book.rotation.set(-.025,-.38+.19*reveal,.025*(1-reveal));
 const poses=[
 [0,[12,13,17],[0,1,0]],[2.0,[12,13,17],[0,1,0]],
 [4.4,[3.0,7.5,10],[-4.0,1.2,.8]],[5.7,[3.0,7.5,10],[-4.0,1.2,.8]],
 [7.0,[5.5,7.0,11],[-1.8,1,2.8]],[9.8,[12.0,8,9],[3.8,1,-.4]],
 [11.7,[9.5,10,13],[.2,1.4,-.5]],[14.0,[9.5,10,13],[.2,1.4,-.5]],
 [17.3,[4.7,4.3,16.8],[.25,2.25,0]],[20,[4.7,4.3,16.8],[.25,2.25,0]]];
 let n=0;while(n<poses.length-2&&t>poses[n+1][0])n++;
 const u=smooth(poses[n][0],poses[n+1][0],t);camera.position.fromArray(poses[n][1].map((v,i)=>lerp(v,poses[n+1][1][i],u)));camera.lookAt(new THREE.Vector3(...poses[n][2].map((v,i)=>lerp(v,poses[n+1][2][i],u))));

 renderer.render(scene,camera);window.__sceneProof={time:t,truck:[...truck.position],grainVisible:particles.filter(p=>p.visible).length,quotePositions:tickets.map(q=>[...q.position]),benchmarkVisible:merge>.5,bookVisible:book.visible,bookScale:book.scale.x,camera:[...camera.position]};
}
export {renderAt};
