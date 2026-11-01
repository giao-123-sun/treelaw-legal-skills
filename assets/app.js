/* All entries are static HTML. JavaScript adds filtering and pagination. */
const form=document.querySelector('#filters');
if(form){
  const cards=[...document.querySelectorAll('.card')],q=document.querySelector('#query'),count=document.querySelector('#count'),empty=document.querySelector('#empty'),sort=document.querySelector('#sort');
  const fields=['task','publisher','system','material','kind','source','access'];
  const labels=['协会','专业律师','法律教师','厂商','个人'];
  const initial=new URLSearchParams(location.search),size=24;
  let current=Math.max(1,parseInt(initial.get('page'),10)||1);
  const metadata=new Map(cards.map(card=>[card,JSON.parse(card.dataset.filter)]));
  const normalize=s=>s.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const texts=new Map(cards.map(card=>[card,normalize(metadata.get(card).text)]));
  for(const key of fields){const el=document.getElementById(key);if([...el.options].some(o=>o.value===initial.get(key)))el.value=initial.get(key);}
  q.value=initial.get('q')||'';
  if(['source','recent','name'].includes(initial.get('sort')))sort.value=initial.get('sort');
  function apply(reset=false){
    if(reset)current=1;
    const words=normalize(q.value).split(' ').filter(Boolean);
    const selected=Object.fromEntries(fields.map(k=>[k,document.getElementById(k).value]));
    const matches=cards.filter(card=>words.every(w=>texts.get(card).includes(w))&&fields.every(k=>!selected[k]||metadata.get(card)[k].includes(selected[k])));
    matches.sort((a,b)=>{const x=metadata.get(a),y=metadata.get(b);if(sort.value==='recent')return y.date.localeCompare(x.date);if(sort.value==='name')return x.name.localeCompare(y.name);return labels.indexOf(x.publisher[0])-labels.indexOf(y.publisher[0]);});
    const pages=Math.max(1,Math.ceil(matches.length/size));current=Math.min(current,pages);
    cards.forEach(card=>card.hidden=true);
    matches.forEach((card,i)=>{card.hidden=i<(current-1)*size||i>=current*size;card.parentNode.appendChild(card);});
    count.textContent=matches.length;empty.hidden=matches.length!==0;
    document.querySelector('#pagination').hidden=matches.length<=size;
    document.querySelector('#previous').disabled=current===1;document.querySelector('#next').disabled=current===pages;
    document.querySelector('#page-label').textContent=`${current} / ${pages}`;
    document.querySelectorAll('[data-kind]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===selected.kind)));
    const params=new URLSearchParams();if(q.value.trim())params.set('q',q.value.trim());
    for(const key of fields)if(selected[key])params.set(key,selected[key]);
    if(sort.value!=='source')params.set('sort',sort.value);if(current>1)params.set('page',current);
    history.replaceState(null,'',location.pathname+(params.size?'?'+params:'')+location.hash);
  }
  form.addEventListener('change',()=>apply(true));q.addEventListener('input',()=>apply(true));sort.addEventListener('change',()=>apply(true));
  document.querySelector('#clear-filters').addEventListener('click',()=>{form.reset();q.value='';sort.value='source';apply(true);});
  document.querySelectorAll('[data-query]').forEach(b=>b.addEventListener('click',()=>{q.value=b.dataset.query;apply(true);q.focus();}));
  document.querySelectorAll('[data-kind]').forEach(b=>b.addEventListener('click',()=>{document.querySelector('#kind').value=b.dataset.kind;apply(true);}));
  for(const [id,delta] of [['previous',-1],['next',1]])document.getElementById(id).addEventListener('click',()=>{current+=delta;apply();document.querySelector('.result-bar').scrollIntoView({block:'start'});});
  apply();
}
