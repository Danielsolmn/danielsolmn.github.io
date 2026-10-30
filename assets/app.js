document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
const filters = document.querySelectorAll('[data-filter]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(other => { const active = other === button; other.classList.toggle('selected', active); other.setAttribute('aria-pressed', String(active)); });
  let count = 0;
  document.querySelectorAll('[data-category]').forEach(card => { const show = button.dataset.filter === 'All' || card.dataset.category.includes(button.dataset.filter); card.hidden = !show; if (show) count++; });
  document.querySelector('.result-count').textContent = `${count} ${count === 1 ? 'project / area' : 'projects / areas'}`;
}));

// Real image links also work without JavaScript. Native dialog provides Escape,
// focus containment, and keyboard support; all captions are inserted as text.
const mediaLinks = document.querySelectorAll('a[data-lightbox]');
if (mediaLinks.length && typeof HTMLDialogElement !== 'undefined') {
  const dialog = document.createElement('dialog');
  dialog.className = 'media-dialog';
  dialog.setAttribute('aria-labelledby', 'media-title');
  dialog.innerHTML = '<div class="media-toolbar"><h2 id="media-title">Project image</h2><button type="button" autofocus>Close ✕</button></div><figure><img alt=""><figcaption></figcaption></figure><a class="media-original" target="_blank" rel="noopener">Open full-resolution image ↗</a>';
  document.body.append(dialog);
  let opener;
  const close = () => dialog.close();
  dialog.querySelector('button').addEventListener('click', close);
  dialog.addEventListener('click', event => { if (event.target === dialog) { const bounds = dialog.getBoundingClientRect(); if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) close(); } });
  dialog.addEventListener('close', () => { document.body.classList.remove('media-open'); opener?.focus(); });
  mediaLinks.forEach(link => link.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const source = link.querySelector('img');
    if (!source) return;
    event.preventDefault(); opener = link;
    const image = dialog.querySelector('img');
    image.src = link.href; image.alt = source.alt;
    dialog.querySelector('figcaption').textContent = link.closest('figure')?.querySelector('figcaption')?.textContent || source.alt;
    dialog.querySelector('.media-original').href = link.href;
    dialog.showModal(); document.body.classList.add('media-open');
  }));
}



// Shared panel/rope coordinates keep the suspension attached throughout sway.
const swayMap = document.querySelector('.balanced-map');
if (swayMap) {
  const panels = ['.map-top','.map-right','.map-about'].map(s=>swayMap.querySelector(s));
  const core=swayMap.querySelector('.central-transistor'), svg=swayMap.querySelector('.sway-ropes');
  const toggle=document.querySelector('#sway-toggle'), status=document.querySelector('#sway-status');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)'), ns='http://www.w3.org/2000/svg';
  let paused=false, visible=true, geometry, frame=0, last=0, elapsed=0;
  const hoverStates=[0,0,0];
  const local=(el,parent)=>{const r=el.getBoundingClientRect();return{x:r.left-parent.left,y:r.top-parent.top,w:r.width,h:r.height};};
  const draw=(motion=true)=>{
    if (!geometry) return;
    const {c,rects,mobile}=geometry;
    const moves=rects.map((r,i)=>{
      const wave=motion?Math.sin(elapsed/([11000,12000,12000][i])*Math.PI*2):0;
      const progress=reduced.matches?1:Math.max(0,Math.min(1,(elapsed-i*110)/1100));
      const eased=1-Math.pow(1-progress,3);
      const target=panels[i].matches(':hover')||panels[i].contains(document.activeElement)?1:0;
      hoverStates[i]+= (target-hoverStates[i])*.14;
      const lift=reduced.matches?0:hoverStates[i];
      const m={x:wave*2.4,y:wave*.8+(1-eased)*16-lift*4,angle:wave*.3,scale:.94+.06*eased+.014*lift};
      panels[i].style.setProperty('transform',`translate(${m.x}px,${m.y}px) rotate(${m.angle}deg) scale(${m.scale})`,'important');
      panels[i].style.opacity=String(.25+.75*eased);return m;
    });
    const point=(p,r,m)=>{const a=m.angle*Math.PI/180,x=(p.x-r.x-r.w/2)*m.scale,y=(p.y-r.y-r.h/2)*m.scale;return{x:r.x+r.w/2+x*Math.cos(a)-y*Math.sin(a)+m.x,y:r.y+r.h/2+x*Math.sin(a)+y*Math.cos(a)+m.y};};

  };
  const measure=()=>{
    panels.forEach(p=>p.style.removeProperty('transform'));
    const bounds=swayMap.getBoundingClientRect();geometry={c:local(core,bounds),rects:panels.map(p=>local(p,bounds)),mobile:matchMedia('(max-width:700px)').matches};
    draw(!reduced.matches);
  };
  const canRun=()=>!paused&&!reduced.matches&&visible&&!document.hidden;
  const tick=now=>{frame=0;if(!canRun()){last=0;return;}if(!last||now-last>=30){elapsed+=last?Math.min(now-last,80):0;last=now;draw();}frame=requestAnimationFrame(tick);};
  const sync=()=>{
    status.textContent=reduced.matches?'Motion off: reduced-motion preference':paused?'Motion paused':'Gentle sway · 10–12 second cycles';
    toggle.hidden=false;toggle.disabled=reduced.matches;toggle.textContent=paused?'Resume motion':'Pause motion';toggle.setAttribute('aria-pressed',String(paused));document.body.classList.toggle('motion-paused',paused);
    if(!canRun()){cancelAnimationFrame(frame);frame=0;last=0;if(reduced.matches)draw(false);}else if(!frame)frame=requestAnimationFrame(tick);
  };
  toggle.addEventListener('click',()=>{paused=!paused;sync();});reduced.addEventListener('change',sync);document.addEventListener('visibilitychange',sync);
  panels.forEach(p=>{p.addEventListener('focusin',sync);p.addEventListener('focusout',()=>requestAnimationFrame(sync));});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();}).observe(swayMap);
  let resizeFrame=0;const schedule=()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(measure);};
  if('ResizeObserver'in window){const observer=new ResizeObserver(schedule);[swayMap,core,...panels].forEach(p=>observer.observe(p));}
  window.addEventListener('resize',schedule,{passive:true});document.fonts?.ready.then(schedule);measure();sync();
}
