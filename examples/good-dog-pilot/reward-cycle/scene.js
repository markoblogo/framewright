import * as T from 'three';
const r=new T.WebGLRenderer({canvas:document.querySelector('canvas'),antialias:true,preserveDrawingBuffer:true});r.setSize(1280,720);r.outputColorSpace=T.SRGBColorSpace;r.toneMapping=T.ACESFilmicToneMapping;r.toneMappingExposure=1.15;
const s=new T.Scene();s.background=new T.Color('#10191d');const c=new T.PerspectiveCamera(35,1280/720,.1,100);c.position.set(1.7,8.8,13.2);c.lookAt(0,.4,.1);
const amber=new T.MeshStandardMaterial({color:'#e8ab53',metalness:.35,roughness:.4}),cyan=new T.MeshStandardMaterial({color:'#69bfc8',metalness:.4,roughness:.35}),white=new T.MeshStandardMaterial({color:'#e7e7d9',roughness:.6}),slate=new T.MeshStandardMaterial({color:'#263d46',metalness:.3,roughness:.5});
function mesh(g,m,x,y,z,parent=s){let o=new T.Mesh(g,m);o.position.set(x,y,z);parent.add(o);return o}
function box(w,h,d,x,y,z,m,parent=s){return mesh(new T.BoxGeometry(w,h,d),m,x,y,z,parent)}
function ball(rad,x,y,z,m,parent=s){return mesh(new T.SphereGeometry(rad,24,16),m,x,y,z,parent)}
const labels=[];
function label(text,x,y,z,width=3.0,size=84){let cv=document.createElement('canvas');cv.width=768;cv.height=160;let ctx=cv.getContext('2d');ctx.fillStyle='#eeeade';ctx.font=`600 ${size}px Arial`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,384,80);let tx=new T.CanvasTexture(cv);tx.colorSpace=T.SRGBColorSpace;let m=new T.MeshBasicMaterial({map:tx,transparent:true,depthWrite:false});let o=mesh(new T.PlaneGeometry(width,width*160/768),m,x,y,z);labels.push(o);return o}
function paw(x,y,z,m,scale=1){let g=new T.Group();g.position.set(x,y,z);g.scale.setScalar(scale);s.add(g);let pad=ball(.28,0,0,0,m,g);pad.scale.set(1,.7,.85);for(let [a,b] of [[-.31,-.28],[-.11,-.43],[.13,-.43],[.33,-.26]]){let toe=ball(.12,a,0,b,m,g);toe.scale.y=.65}return g}
box(13,.12,9,0,-.2,.3,new T.MeshStandardMaterial({color:'#14262d',roughness:.8}));
let nodes=[];for(let x of [-4,0,4]){let disc=mesh(new T.CylinderGeometry(1.1,1.15,.24,64),slate,x,.05,0);let ring=mesh(new T.TorusGeometry(1.11,.025,8,64),cyan,x,.19,0);ring.rotation.x=-Math.PI/2;nodes.push({disc,ring})}
paw(-4,.3,-.1,amber,1.5);box(.55,.16,.4,-3.45,.3,.45,white);
// Abstract bowl and reward token, not an instruction about real substances.
mesh(new T.CylinderGeometry(.55,.35,.26,40,1,true),white,0,.32,0);let reward=ball(.2,0,.72,0,amber);
const human=new T.Group();human.position.set(4,.18,0);s.add(human);ball(.22,0,1,0,white,human);box(.42,.65,.22,0,.48,0,white,human);for(let x of [-.15,.15])box(.12,.4,.15,x,.02,0,white,human);
label('FIND',-4,1.55,0);label('REWARD',0,1.6,0);label('REPEAT',4,1.6,0);
const path=new T.CatmullRomCurve3([new T.Vector3(-4,.28,1.6),new T.Vector3(0,.28,1.6),new T.Vector3(4,.28,1.6),new T.Vector3(5.1,.28,2.6),new T.Vector3(0,.28,3.3),new T.Vector3(-5.1,.28,2.6)],true);
mesh(new T.TubeGeometry(path,160,.025,8,true),new T.MeshBasicMaterial({color:'#557e88'}),0,0,0);
const packets=[box(.36,.14,.24,0,.5,0,amber),box(.36,.14,.24,0,.5,0,white)];
for(let x of [-2,2]){let a=mesh(new T.ConeGeometry(.12,.32,3),amber,x,.3,1.6);a.rotation.z=-Math.PI/2}
const control=new T.Group();s.add(control);let ctrl=mesh(new T.CylinderGeometry(.65,.7,.22,40),cyan,0,.25,-3.4,control);const pawControl=paw(0,.45,-3.4,amber,1.15);let ctrlLabel=label('CONTROL',0,1.65,-3.4,2.8,75);
const wire=new T.CatmullRomCurve3([new T.Vector3(0,.35,-2.9),new T.Vector3(0,.35,-1.8),new T.Vector3(0,.35,-.65)]);let line=mesh(new T.TubeGeometry(wire,20,.04,8,false),amber,0,0,0);line.visible=false;
s.add(new T.HemisphereLight('#bed8e1','#203039',2.3));let light=new T.DirectionalLight('#ffcf8c',4);light.position.set(-4,8,6);s.add(light);let rim=new T.DirectionalLight('#77c8dc',2);rim.position.set(5,5,-4);s.add(rim);
const smooth=(a,b,t)=>{let u=T.MathUtils.clamp((t-a)/(b-a),0,1);return u*u*(3-2*u)};
function renderAt(t){t=T.MathUtils.clamp(t,0,5.999);for(let i=0;i<packets.length;i++){let u=(t*.18+i*.5)%1;packets[i].position.copy(path.getPointAt(u));packets[i].position.y=.42;let v=path.getTangentAt(u);packets[i].rotation.y=-Math.atan2(v.z,v.x)}
reward.position.y=.7+.06*Math.sin(t*3);human.rotation.z=.025*Math.sin(t*4);let show=smooth(3.5,4.4,t);control.scale.setScalar(Math.max(.001,show));pawControl.scale.setScalar(Math.max(.001,show)*1.15);ctrlLabel.material.opacity=show;line.visible=show>.5;
for(let i=0;i<3;i++){let pulse=.5+.5*Math.sin(t*2.5-i*1.5);nodes[i].ring.material=i===1&&show>.5?amber:cyan;nodes[i].ring.scale.setScalar(1+pulse*.025)}
c.position.set(1.7-1.1*smooth(0,6,t),8.8,13.2);c.lookAt(0,.4,.3);for(let l of labels)l.quaternion.copy(c.quaternion);r.render(s,c);window.currentTime=t;}
window.renderAt=renderAt;window.sceneReady=true;renderAt(0);
