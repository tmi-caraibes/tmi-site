# Audit mobile : débordement horizontal, éléments plus larges que l'écran, chevauchements de texte, captures.
import asyncio, os, json
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8765'
PAGES = ['/', '/entreprise/', '/expertises/', '/realisations/', '/materiel/', '/engagements/', '/carrieres/', '/contact/',
         '/mentions-legales/', '/enrobes-voirie-guadeloupe-saint-martin/', '/reseaux-eau-potable-assainissement-guadeloupe/',
         '/vrd-terrassement-guadeloupe/', '/fondations-speciales-parasismique-guadeloupe/', '/batiment-genie-civil-guadeloupe/',
         '/chantier-enrobe-friars-bay-saint-martin/', '/chantier-aep-quai-6-port-guadeloupe/', '/404.html',
         '/en/', '/en/projects/', '/en/asphalt-paving-roadworks-guadeloupe-saint-martin/', '/en/contact/', '/en/legal-notice/']

JS_CHECK = r'''() => {
  const vw = document.documentElement.clientWidth;
  const out = {scrollW: document.documentElement.scrollWidth, vw, wide: [], overlaps: []};
  const els = [...document.querySelectorAll('body *')];
  for (const el of els) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.left > -1000 && (r.right > vw + 1 || r.left < -1) && getComputedStyle(el).position !== 'fixed') {
      out.wide.push({tag: el.tagName.toLowerCase(), cls: el.className && el.className.baseVal === undefined ? el.className : '', left: Math.round(r.left), right: Math.round(r.right)});
      if (out.wide.length > 8) break;
    }
  }
  // chevauchement entre éléments de texte frères visibles (hors positionnement absolu voulu)
  const textEls = els.filter(e => ['A','STRONG','SPAN','P','H1','H2','H3','H4','LI','DD','DT','BUTTON'].includes(e.tagName)
      && e.children.length === 0 && e.textContent.trim().length > 2 && getComputedStyle(e).position === 'static' && !(e.closest('details:not([open])') && e.tagName !== 'SUMMARY') && e.getBoundingClientRect().left > -1000);
  const boxes = textEls.map(e => ({e, r: e.getBoundingClientRect()})).filter(b => b.r.width > 0 && b.r.height > 0);
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
    const oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ox > 6 && oy > 6) {
      out.overlaps.push([a.e.textContent.trim().slice(0, 40), b.e.textContent.trim().slice(0, 40)]);
      if (out.overlaps.length > 6) return out;
    }
  }
  return out;
}'''

async def main():
    os.makedirs('/home/claude/shots/mobile', exist_ok=True)
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (360, 390, 430):
            ctx = await b.new_context(viewport={'width': w, 'height': 800}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = await ctx.new_page()
            for path in PAGES:
                await pg.goto(BASE + path, wait_until='load')
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(300)
                await pg.evaluate("window.scrollTo(0, 0)"); await pg.wait_for_timeout(100)
                res = await pg.evaluate(JS_CHECK)
                key = f'{w} {path}'
                probs = {}
                if res['scrollW'] > res['vw'] + 1: probs['debordement'] = f"{res['scrollW']}px > {res['vw']}px"
                if res['wide']: probs['trop_larges'] = res['wide'][:5]
                if res['overlaps']: probs['chevauchements'] = res['overlaps'][:5]
                if probs: report[key] = probs
                if w == 390:
                    await pg.screenshot(path=f"/home/claude/shots/mobile/{path.strip('/').replace('/', '_') or 'index'}.png", full_page=True)
            await ctx.close()
        await b.close()
    print(json.dumps(report, ensure_ascii=False, indent=1) if report else 'aucun problème détecté')

asyncio.run(main())
