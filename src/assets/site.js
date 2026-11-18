/* TMI — scripts communs : menu, réalisations, formulaires, vidéos */
(function(){
  var lang = (document.documentElement.lang||'fr').slice(0,2);
  var fmt = function(n){
    return new Intl.NumberFormat(lang==='fr'?'fr-FR':'en-GB',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n);
  };

  // ---------- Menu mobile ----------
  var head=document.querySelector('.head'), burger=head&&head.querySelector('.burger');
  if(burger){
    burger.addEventListener('click',function(){
      var open=!head.classList.contains('open');
      head.classList.toggle('open',open); burger.setAttribute('aria-expanded',String(open));
    });
  }

  // ---------- Réalisations : filtres + fiche ----------
  var grid=document.getElementById('refs-grid');
  if(grid){
    var cards=[].slice.call(grid.querySelectorAll('.card')), current='all';
    var update=function(){
      var n=0,sum=0;
      cards.forEach(function(c){
        var show=current==='all'||c.dataset.cat===current;
        c.hidden=!show; if(show){n++;sum+=+c.dataset.amt;}
      });
      var cnt=document.getElementById('refs-count'), tot=document.getElementById('refs-sum');
      if(cnt) cnt.textContent = lang==='fr' ? n+(n>1?' chantiers présentés':' chantier présenté') : n+(n>1?' projects shown':' project shown');
      if(tot) tot.textContent = fmt(sum);
      document.querySelectorAll('.filters button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.cat===current))});
    };
    window.__refsUpdate=update;
    document.querySelectorAll('.filters button').forEach(function(b){
      b.addEventListener('click',function(){current=b.dataset.cat;update()});
    });
    var h=location.hash.replace('#','');
    if(['reseaux','voirie','fondations','batiment'].indexOf(h)>-1) current=h;
    update();
  }

  // ---------- Formulaires (Netlify) ----------
  document.querySelectorAll('form[data-netlify]').forEach(function(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=form.parentNode.querySelector('.form-msg:not(.err)'), err=form.parentNode.querySelector('.form-msg.err');
      ok.hidden=true; err.hidden=true;
      var data=new FormData(form), hasFile=!!form.querySelector('input[type=file]');
      var opts=hasFile?{method:'POST',body:data}:{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data).toString()};
      fetch('/',opts).then(function(r){if(!r.ok) throw new Error(r.status); form.hidden=true; ok.hidden=false;})
        .catch(function(){err.hidden=false;});
    });
  });

  var y=document.getElementById('year'); if(y) y.textContent=new Date().getFullYear();
})();

// ---------- Vidéos YouTube (chargées au clic) ----------
document.querySelectorAll('.yt[data-yt]').forEach(function(b){
  b.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label')||'Vidéo';
    f.allow='autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen=true;
    f.className='yt-frame'; b.replaceWith(f);
  });
});
