import fs from 'fs';
import vm from 'vm';
const src = fs.readFileSync('/Users/aayankhare/Claude/Projects/QuanticaEdu/landing.html','utf8');
const start = src.indexOf('var PSET_CHALLENGE_NOTE');
const end = src.indexOf('var completed={');
const code = src.slice(start, end);
const sandbox = { window:{}, document:{ getElementById:()=>null, querySelector:()=>null, createElement:()=>({style:{},classList:{add(){},remove(){}},addEventListener(){},setAttribute(){}}) }, location:{pathname:'',search:''}, history:{pushState(){}}, Object, console };
vm.createContext(sandbox);
try { vm.runInContext(code, sandbox); } catch(e) { console.error('eval stopped at:', e.message); }
const PSETS = vm.runInContext('typeof PSETS!=="undefined"?PSETS:null', sandbox);
if(!PSETS){ console.error('PSETS not captured'); process.exit(1); }
const chapters = Object.keys(PSETS).map(Number).sort((a,b)=>a-b);
console.log('PSETS chapters:', chapters.join(','));
let totalP=0,totalC=0, problems=[];
const issues=[];
for(const ch of chapters){
  const s=PSETS[ch];
  const p=(s.practice||[]).length, c=(s.challenge||[]).length;
  totalP+=p; totalC+=c;
  const legendary=(s.challenge||[]).filter(r=>r.legendary).length;
  const legendaryInPractice=(s.practice||[]).filter(r=>r.legendary).length;
  console.log(`ch${ch}: practice=${p} challenge=${c} legendary-in-challenge=${legendary} legendary-in-practice=${legendaryInPractice}`);
  for(const [type,arr] of [['practice',s.practice||[]],['challenge',s.challenge||[]]]){
    arr.forEach((r,i)=>{
      const id=`ch${ch}.${type}[${i}]`;
      if(r.o){ issues.push(`${id}: legacy multiple-choice format (o array)`); return; }
      if(r.ans===undefined||r.ans===null||r.ans==='') issues.push(`${id}: missing/empty ans`);
      if(!r.sol) issues.push(`${id}: missing sol`);
      if(!r.x&&!r.q) issues.push(`${id}: missing problem text`);
      // KaTeX checks on rendered fields
      for(const [f,v] of [['x',r.x],['sol',r.sol],...( (r.hints||[]).map((h,j)=>[`hints[${j}]`,h]) )]){
        if(typeof v!=='string') continue;
        if((v.match(/\\\(/g)||[]).length !== (v.match(/\\\)/g)||[]).length) issues.push(`${id}.${f}: mismatched \\( \\)`);
        if(((v.match(/\$\$/g)||[]).length)%2===1) issues.push(`${id}.${f}: odd $$ count`);
        const s2=v.replace(/\\\$/g,'').replace(/\$\$/g,'');
        if((s2.match(/\$/g)||[]).length%2===1) issues.push(`${id}.${f}: odd single-$`);
        // prose swallowed in single-$ span
        const spans=[...s2.matchAll(/\$([^$]*)\$/g)].map(m=>m[1]);
        for(const sp of spans){ const stripped=sp.replace(/\\[a-zA-Z]+/g,''); if(/[a-zA-Z]{3,}\s+[a-zA-Z]{3,}/.test(stripped)) issues.push(`${id}.${f}: prose inside $...$: "${sp.slice(0,60)}"`); }
      }
    });
  }
}
console.log(`totals: practice=${totalP} challenge=${totalC}`);
console.log('issues:', issues.length);
issues.forEach(x=>console.log(' -',x));
