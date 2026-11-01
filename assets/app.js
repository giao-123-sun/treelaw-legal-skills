/* All content is prerendered. JavaScript only filters existing entries. */
const form=document.querySelector('#filters');
if(form){
  const cards=[...document.querySelectorAll('.card')], q=document.querySelector('#query'), count=document.querySelector('#count'), empty=document.querySelector('#empty'), sort=document.querySelector('#sort');
  const fields=['task','publisher','system','material','kind','access'];
  const labels=['协会','专业律师','法律教师','厂商','个人'];
  const initial=new URLSearchParams(location.search);
  for(const key of fields){const el=document.getElementById(key);if([...el.options].some(o=>o.value===initial.get(key)))el.value=initial.get(key);}
  q.value=initial.get('q')||'';
  if(['source','recent','name'].includes(initial.get('sort')))sort.value=initial.get('sort');
  const normalize=s=>s.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  function apply(){
    const words=normalize(q.value).split(' ').filter(Boolean);
    let shown=0;
    for(const card of cards){
      const data=JSON.parse(card.dataset.filter);
      card.hidden=!(words.every(w=>normalize(data.text).includes(w))&&fields.every(k=>!document.getElementById(k).value||data[k].includes(document.getElementById(k).value)));
      if(!card.hidden)shown++;
    }
    const ordered=[...cards].sort((a,b)=>{
      const x=JSON.parse(a.dataset.filter),y=JSON.parse(b.dataset.filter);
      if(sort.value==='recent')return y.date.localeCompare(x.date);
      if(sort.value==='name')return x.name.localeCompare(y.name);
      return labels.indexOf(x.publisher[0])-labels.indexOf(y.publisher[0]);
    });
    for(const card of ordered)card.parentNode.appendChild(card);
    count.textContent=shown;
    empty.hidden=shown!==0;
    const params=new URLSearchParams();
    if(q.value.trim())params.set('q',q.value.trim());
    for(const key of fields)if(document.getElementById(key).value)params.set(key,document.getElementById(key).value);
    if(sort.value!=='source')params.set('sort',sort.value);
    history.replaceState(null,'',location.pathname+(params.size?'?'+params:'')+location.hash);
  }
  form.addEventListener('change',apply);q.addEventListener('input',apply);sort.addEventListener('change',apply);
  document.querySelector('#clear-filters').addEventListener('click',()=>{form.reset();q.value='';sort.value='source';apply();});
  document.querySelectorAll('[data-query]').forEach(b=>b.addEventListener('click',()=>{q.value=b.dataset.query;apply();q.focus();}));
  apply();
}
