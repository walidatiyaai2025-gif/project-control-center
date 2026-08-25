const esc=v=>String(v??'—').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const short=v=>v?String(v).slice(0,10):'—';
const pair=(version,sha)=>version?`${esc(version)} @ ${esc(short(sha))}`:esc(short(sha));
async function run(){
 const r=await fetch('../portfolio/status/index.json');const d=await r.json();
 document.getElementById('meta').textContent=`Control plane ${d.CONTROL_PLANE_VERSION} • generated ${d.GENERATED_AT||'not yet'}`;
 const metrics=['TOTAL_PROJECTS','HEALTHY','NEEDS_ATTENTION','CRITICAL','ACTIVE_TASKS','WAITING_FOR_USER','UNTRACKED_REQUESTS','VERSION_DRIFT_PROJECTS'];
 document.getElementById('cards').innerHTML=metrics.map(k=>`<div class="card"><div>${k.replaceAll('_',' ')}</div><div class="n">${d[k]??0}</div></div>`).join('');
 document.getElementById('rows').innerHTML=(d.PROJECTS||[]).map(p=>`<tr><td>${esc(p.PROJECT_ID)}</td><td>${esc(p.HEALTH)}</td><td>${esc(p.PROGRESS)}</td><td>${pair(p.CURRENT_PRODUCTION_VERSION,p.PRODUCTION_SHA)}</td><td>${pair(p.CURRENT_DEVELOPMENT_VERSION||p.TARGET_DEVELOPMENT_VERSION,p.CANONICAL_INTEGRATION_SHA)}</td><td>${esc(p.NEXT_RELEASE_CANDIDATE)}</td><td>${esc(p.LATEST_USER_REVIEW_CANDIDATE)}</td><td>${esc(p.P0??0)}</td><td>${esc(p.BLOCKED??0)}</td><td>${esc(p.QA??0)}</td><td>${esc(p.STALE??0)}</td><td>${esc(p.WAITING_FOR_USER??0)}</td><td>${esc((p.DRIFT||[]).join(', '))}</td><td>${esc(p.LAST_SYNC)}</td><td>${esc(p.CONTROL_PLANE_MATURITY)}</td><td>${esc(p.CONTROL_PLANE_VERSION)}</td></tr>`).join('');
}
run().catch(e=>document.getElementById('meta').textContent='Dashboard data unavailable: '+e.message);
