# Vérification du site dist/ via le serveur local : liens, images, console (CSP), textes FR restants en EN, choix des images sur mobile
import asyncio, re, sys, json
from urllib.parse import urljoin, urlsplit
from playwright.async_api import async_playwright
import urllib.request

BASE = 'http://127.0.0.1:8765'
FR_HINT = re.compile(r"[éèàùçêô]|\b(les|des|de la|du|nous|chantier|réalis|avec|pour)\b", re.I)

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
_opener = urllib.request.build_opener(_NoRedirect)
def head_status(url):
    try:
        r = _opener.open(urllib.request.Request(url, method='GET'), timeout=10)
        return r.status, r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.headers

async def main():
    seen, queue = set(), ['/']
    broken, console_errs, fr_left, img_bad, mobile_pick = [], [], {}, [], {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        pg = await ctx.new_page()
        pg.on('console', lambda m: console_errs.append((pg.url, m.type, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: console_errs.append((pg.url, 'pageerror', str(e))))
        links_all = set()
        while queue:
            path = queue.pop(0)
            if path in seen: continue
            seen.add(path)
            resp = await pg.goto(BASE + path, wait_until='load')
            if resp.status != 200:
                broken.append((path, resp.status)); continue
            await pg.wait_for_timeout(150)
            lang = await pg.evaluate("document.documentElement.lang")
            hrefs = await pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
            for h in hrefs:
                if h.startswith(('mailto:', 'http', '#', 'tel:')): continue
                u = urlsplit(urljoin(path, h)).path
                links_all.add((path, h, u))
                if u not in seen and u not in queue: queue.append(u)
            # images
            bad = await pg.evaluate("[...document.images].filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src'))")
            await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(400)
            bad = await pg.evaluate("[...document.images].filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src'))")
            if bad: img_bad.append((path, bad))
            if lang == 'en':
                txt = await pg.evaluate('''()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(t.length>20)out.push(t)}return out}''')
                sus = [t[:70] for t in txt if FR_HINT.search(t) and 'TMI Travaux' not in t and 'Route de l' not in t and 'Petit-Bourg' not in t]
                if sus: fr_left[path] = sus[:6]
        # liens cassés (status HTTP)
        checked = {}
        for src, h, u in sorted(links_all):
            if u not in checked:
                checked[u] = head_status(BASE + u)[0]
            if checked[u] != 200: broken.append((src, h, checked[u]))
        # choix d'image sur mobile
        m = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        mp = await m.new_page()
        for path in ['/', '/enrobes-voirie-guadeloupe-saint-martin/', '/en/projects/']:
            await mp.goto(BASE + path, wait_until='load'); await mp.wait_for_timeout(300)
            mobile_pick[path] = await mp.evaluate("[...document.querySelectorAll('picture img')].slice(0,5).map(i=>i.currentSrc.split('/').pop())")
        await b.close()
    print('pages visitées :', len(seen))
    print('liens cassés :', broken)
    print('images non chargées :', img_bad)
    print('console :', [c for c in console_errs if 'favicon' not in c[2]][:10])
    print('FR restant en EN :', json.dumps(fr_left, ensure_ascii=False, indent=1)[:1500])
    print('images choisies sur mobile :', mobile_pick)
    # redirections anciennes adresses
    for old in ['/entreprise.html', '/index.html', '/chantier-enrobe-friars-bay-saint-martin.html', '/nimporte-quoi']:
        st, hd = head_status(BASE + old)
        print('redir', old, st, hd.get('Location'))
    st, hd = head_status(BASE + '/')
    print('CSP :', hd.get('Content-Security-Policy')[:60], '| cache html :', hd.get('Cache-Control'))
    print('cache assets :', head_status(BASE + '/assets/style.css')[1].get('Cache-Control'))

asyncio.run(main())
