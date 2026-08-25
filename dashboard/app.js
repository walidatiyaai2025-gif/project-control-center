const esc=v=>String(v??'—').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const short=v=>v?String(v).slice(0,10):'—';
const num=(p,k)=>esc(p[k]??0);
async function run(){
 const r=await fetch('../portfolio/status/index.json'); const d=await r.json();
 document.getElementById('meta').textContent=`Control plane ${d.CONTROL_PLANE_VERSION} • generated ${d.GENERATED_AT||'not yet'}`;
 const metrics=['TOTAL_PROJECTS','COLLECTION_PASS','DISCOVERED','BASELINE_LOCKED','CANARY_PROJECTS','DRIFT_PROJECTS','TOTAL_BRANCHES','TOTAL_OPEN_PRS','FEATURES_IMPLEMENTED_NOT_CONNECTED','FALSE_DONE_FEATURES'];
 document.getElementById('cards').innerHTML=metrics.map(k=>`<div class="card"><div>${k.replaceAll('_',' ')}</div><div class="n">${d[k]??0}</div></div>`).join('');
 document.getElementById('rows').innerHTML=(d.PROJECTS||[]).map(p=>`<tr><td>${esc(p.PROJECT_ID)}</td><td>${esc(p.HEALTH)}</td><td>${esc(p.POLICY_ENFORCEMENT_MODE)}</td><td>${esc(p.COLLECTOR_RESULT)}</td><td>${esc(p.DISCOVERY_COMPLETE)}</td><td>${esc(p.BASELINE_LOCKED)}</td><td>${esc(p.DEFAULT_BRANCH)} @ ${esc(short(p.DEFAULT_BRANCH_SHA))}</td><td>${num(p,'BRANCH_COUNT')}</td><td>${esc(p.OPEN_PR_COUNT)}</td><td>${esc((p.DRIFT||[]).length)}</td><td>${esc(p.CONTROL_PLANE_VERSION)}</td></tr>`).join('');
 document.getElementById('project-details').innerHTML=(d.PROJECTS||[]).map(p=>`<section class="project"><h2>${esc(p.DISPLAY_NAME||p.PROJECT_ID)}</h2><p><b>Fleet:</b> ${esc(p.ENROLLMENT_STATE)} • ${esc(p.POLICY_ENFORCEMENT_MODE)} • canary=${esc(p.CANARY)} • writeAuthorized=${esc(p.WRITE_AUTHORIZED)}</p><p><b>Discovery:</b> ${esc(p.COLLECTOR_RESULT)} • complete=${esc(p.DISCOVERY_COMPLETE)} • baseline=${esc(p.BASELINE_LOCKED)} • targetMutated=${esc(p.TARGET_MUTATED)}</p><p><b>Repository:</b> ${esc(p.REPOSITORY)} • default=${esc(p.DEFAULT_BRANCH)} @ ${esc(short(p.DEFAULT_BRANCH_SHA))} • branches=${num(p,'BRANCH_COUNT')} • openPRs=${esc(p.OPEN_PR_COUNT)}</p><p><b>Drift:</b> ${(p.DRIFT||[]).map(x=>`<span class="pill">${esc(typeof x==='string'?x:(x.TYPE||JSON.stringify(x)))}</span>`).join('')||'—'}</p><p><b>Feature governance retained:</b> implemented-not-connected ${num(p,'FEATURES_IMPLEMENTED_NOT_CONNECTED')} • false-done ${num(p,'FALSE_DONE_FEATURES')}</p></section>`).join('');
}
run().catch(e=>document.getElementById('meta').textContent='Dashboard data unavailable: '+e.message);
