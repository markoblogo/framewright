// Original reusable absolute-time camera sampler; no renderer/provider calls.
export function validateCameraPlan(plan){
 if(!plan||![plan.width,plan.height,plan.fps,plan.seconds].every(x=>Number.isFinite(x)&&x>0)||!Array.isArray(plan.shots)||!plan.shots.length)throw Error('Positive canvas/timebase and nonempty shot plan required');
 let end=0;const ids=new Set();
 for(const s of plan.shots){
  if(!s.id||ids.has(s.id)||!s.scene||!Number.isFinite(s.start)||!Number.isFinite(s.end)||Math.abs(s.start-end)>1e-9||s.end<=s.start)throw Error('Unique contiguous positive-duration shots required');
  if(!Number.isFinite(s.fov)||s.fov<=0||s.fov>=179||![s.from,s.to,s.look_from,s.look_to].every(a=>Array.isArray(a)&&a.length===3&&a.every(Number.isFinite)))throw Error('Finite camera triples and valid field of view required');
  ids.add(s.id);end=s.end;
 }
 if(Math.abs(end-plan.seconds)>1e-9)throw Error('Shot durations must match master duration');
 return plan;
}
export function sampleCamera(plan,t){
 if(!Number.isFinite(t))throw Error('Finite time required');
 const shot=plan.shots.find(s=>t>=s.start&&t<s.end)||(t>=plan.seconds?plan.shots.at(-1):plan.shots[0]);
 const x=Math.max(0,Math.min(1,(t-shot.start)/(shot.end-shot.start))),u=x*x*(3-2*x),blend=(a,b)=>a.map((v,i)=>v+(b[i]-v)*u);
 return {id:shot.id,scene:shot.scene,fov:shot.fov,position:blend(shot.from,shot.to),target:blend(shot.look_from,shot.look_to)};
}
