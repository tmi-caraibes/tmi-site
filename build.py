#!/usr/bin/env python3
"""Génère le site TMI : python3 build.py → dist/ (Netlify) et preview/ (aperçu à plat)."""
from html import escape as esc
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')       # CSS, JS, polices, images sources (jpg/png)
DIST = os.path.join(HERE, 'dist')     # site prêt pour Netlify (adresses propres, FR + EN) — dossier publié
OUT = os.path.join(HERE, 'preview')   # aperçu à plat (fichiers .html, liens relatifs) pour l'artefact Claude
BASE = 'https://tmi-caraibes.com/'
LANG = 'fr'                         # langue en cours de génération
import hashlib
def _h(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]
CSS_V = _h(SRC + '/assets/style.css')
JS_V = _h(SRC + '/assets/site.js')

# Adresses anglaises (sans .html)
EN_SLUG = {
    'index.html': '', 'entreprise.html': 'company', 'expertises.html': 'expertise', 'realisations.html': 'projects',
    'materiel.html': 'equipment', 'engagements.html': 'commitments', 'carrieres.html': 'careers', 'contact.html': 'contact',
    'mentions-legales.html': 'legal-notice', '404.html': '404',
    'reseaux-eau-potable-assainissement-guadeloupe.html': 'water-supply-sewer-networks-guadeloupe-saint-martin',
    'enrobes-voirie-guadeloupe-saint-martin.html': 'asphalt-paving-roadworks-guadeloupe-saint-martin',
    'vrd-terrassement-guadeloupe.html': 'earthworks-utilities-guadeloupe',
    'fondations-speciales-parasismique-guadeloupe.html': 'special-foundations-seismic-strengthening-guadeloupe',
    'batiment-genie-civil-guadeloupe.html': 'building-civil-engineering-guadeloupe',
    'chantier-aep-assainissement-cornet-petit-canal.html': 'project-water-sewer-networks-cornet-petit-canal',
    'chantier-enrobe-rue-de-hollande-marigot.html': 'project-asphalt-rue-de-hollande-marigot',
    'chantier-enrobe-friars-bay-saint-martin.html': 'project-asphalt-friars-bay-saint-martin',
    'chantier-enrobe-rue-colombier-saint-martin.html': 'project-asphalt-rue-colombier-saint-martin',
    'chantier-enrobe-froston-saint-martin.html': 'project-asphalt-froston-saint-martin',
    'chantier-pont-de-vanier-vieux-habitants.html': 'project-vanier-bridge-vieux-habitants',
    'chantier-amenagement-securisation-vieux-fort.html': 'project-roadworks-safety-vieux-fort',
    'chantier-amenagement-voirie-capesterre-belle-eau.html': 'project-roadworks-capesterre-belle-eau',
    'chantier-travaux-urgence-soufriere-saint-claude.html': 'project-emergency-works-soufriere-saint-claude',
    'chantier-renforcement-parasismique-bergevin-pointe-a-pitre.html': 'project-seismic-strengthening-bergevin-pointe-a-pitre',
    'chantier-confortement-talus-vieux-fort.html': 'project-slope-stabilisation-vieux-fort',
    'chantier-micropieux-belle-plaine-le-gosier.html': 'project-micropiles-belle-plaine-le-gosier',
    'chantier-mur-soutenement-spring-saint-martin.html': 'project-retaining-wall-spring-saint-martin',
    'chantier-rehabilitation-class-vieux-habitants.html': 'project-class-building-vieux-habitants',
    'chantier-creche-vieux-habitants.html': 'project-nursery-vieux-habitants',
    'chantier-aep-quai-6-port-guadeloupe.html': 'project-water-supply-quay-6-port-guadeloupe',
    'chantier-confortement-parasismique-legitimus.html': 'project-seismic-strengthening-legitimus',
}
def path_for(page, lang):
    """Chemin depuis la racine du site, ex. /entreprise/ ou /en/company/."""
    if page == '404.html':
        return '/404.html'
    if lang == 'fr':
        return '/' if page == 'index.html' else '/' + page[:-5] + '/'
    return '/en/' if page == 'index.html' else '/en/' + EN_SLUG[page] + '/'
def url_for(page, lang):
    return BASE.rstrip('/') + path_for(page, lang)

def a(s):  # attribute-safe
    return esc(s, quote=True)

def T(fr, en, tag='span', cls=None, html=False, **attrs):
    c = f' class="{cls}"' if cls else ''
    extra = ''.join(f' {k.replace("_","-")}="{a(v)}"' for k, v in attrs.items())
    if html:
        return f'<{tag}{c}{extra} data-en-html="{a(en)}">{fr}</{tag}>'
    return f'<{tag}{c}{extra} data-en="{a(en)}">{esc(fr)}</{tag}>'

IMG_WIDTHS = (480, 800, 1200)
_IMG_DIMS = {}
def img_dims(name):
    if name not in _IMG_DIMS:
        from PIL import Image
        _IMG_DIMS[name] = Image.open(f'{SRC}/img/{name}.jpg').size
    return _IMG_DIMS[name]
def img_variants(name):
    """Largeurs réellement générées pour une image (jamais plus large que la source)."""
    w0 = img_dims(name)[0]
    ws = [w for w in IMG_WIDTHS if w < w0] + [w0]
    return ws
SIZES_DEFAULT = '(max-width:700px) 100vw, (max-width:1100px) 50vw, 400px'
def pic(name, alt_fr, alt_en, w=None, h=None, lazy=True, cls=None, prio=False, sizes=None):
    w0, h0 = img_dims(name)
    dims = f' width="{w0}" height="{h0}"'
    ld = ' loading="lazy" decoding="async"' if lazy else ''
    fp = ' fetchpriority="high"' if prio else ''
    c = f' class="{cls}"' if cls else ''
    ws = img_variants(name)
    srcset = ', '.join(f'/img/{name}-{x}.webp {x}w' for x in ws)
    fallback = [x for x in ws if x >= 800][0] if any(x >= 800 for x in ws) else ws[-1]
    sz = sizes or SIZES_DEFAULT
    return (f'<picture{c}><img src="/img/{name}-{fallback}.webp" srcset="{srcset}" sizes="{sz}"'
            f' alt="{a(alt_fr)}" data-en-alt="{a(alt_en)}"{dims}{ld}{fp}></picture>')

NAV = [
    ('entreprise.html', 'Entreprise', 'Company'),
    ('expertises.html', 'Expertises', 'Expertise'),
    ('realisations.html', 'Réalisations', 'Projects'),
    ('materiel.html', 'Matériel', 'Equipment'),
    ('engagements.html', 'Engagements', 'Commitments'),
    ('carrieres.html', 'Carrières', 'Careers'),
]

ADDR_FR = "Route de l'Hôtel, Tambour Monplaisir<br>97170 Petit-Bourg, Guadeloupe"
EMAIL = 'contact@tmi-caraibes.com'

def head(page, title, desc, extra_ld=None, nav_page=None, title_en=None, desc_en=None, extra_ld_en=None):
    lang = LANG
    url = url_for(page, lang)
    url_fr, url_en = url_for(page, 'fr'), url_for(page, 'en')
    if lang == 'en':
        title = title_en or title
        desc = desc_en or desc
        if extra_ld_en is not None:
            extra_ld = extra_ld_en
    ld = {
        "@context": "https://schema.org", "@type": "GeneralContractor",
        "name": "TMI Travaux Modernes Ingénierie", "url": BASE,
        "logo": BASE + "img/logo-tmi.png", "image": BASE + "img/hero-voirie.jpg",
        "email": EMAIL, "foundingDate": "2023",
        "address": {"@type": "PostalAddress", "streetAddress": "Route de l'Hôtel, Tambour Monplaisir",
                    "postalCode": "97170", "addressLocality": "Petit-Bourg", "addressRegion": "Guadeloupe", "addressCountry": "FR"},
        "areaServed": ["Guadeloupe", "Saint-Martin"]}
    ld["image"] = BASE + "img/og-tmi.jpg"
    ld["inLanguage"] = lang
    ldjson = json.dumps(ld, ensure_ascii=False) if page == 'index.html' else ''
    if extra_ld:
        ldjson = json.dumps(extra_ld, ensure_ascii=False)
    cur = nav_page or page
    alt = ('' if page == '404.html' else
           f'<link rel="alternate" hreflang="fr" href="{url_fr}">\n<link rel="alternate" hreflang="en" href="{url_en}">\n<link rel="alternate" hreflang="x-default" href="{url_fr}">\n')
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{a(desc)}">
<link rel="canonical" href="{url}">
{alt}<meta property="og:type" content="website">
<meta property="og:site_name" content="TMI Travaux Modernes Ingénierie">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og-tmi.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'en_GB' if lang == 'en' else 'fr_FR'}">
<meta property="og:locale:alternate" content="{'fr_FR' if lang == 'en' else 'en_GB'}">
<link rel="icon" type="image/png" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={CSS_V}">
{f'<script type="application/ld+json">{ldjson}</script>' if ldjson else ''}
</head>
<body>
<a class="skip" href="#main" data-en="Skip to content">Aller au contenu</a>
<div class="util"><div class="wrap">
  {T("Travaux publics en Guadeloupe et à Saint-Martin", "Public works in Guadeloupe and Saint-Martin")}
  <div class="util-right">
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="carrieres.html" data-en="Join us">Nous rejoindre</a>
    <nav class="lang" aria-label="Langue / Language">
      <a href="{path_for(page, 'fr')}" hreflang="fr" lang="fr"{' aria-current="true"' if lang == 'fr' else ''} title="Version française">FR</a>
      <a href="{path_for(page, 'en')}" hreflang="en" lang="en"{' aria-current="true"' if lang == 'en' else ''} title="English version">EN</a>
    </nav>
  </div>
</div></div>
<header class="head"><div class="wrap">
  <a href="index.html" class="logo"><img src="/img/logo-tmi.png" alt="TMI Travaux Modernes Ingénierie, accueil" data-en-alt="TMI Travaux Modernes Ingénierie, home" width="166" height="44"></a>
  <ul class="nav" id="nav">
    {''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""} data-en="{a(en)}">{esc(fr)}</a></li>' for h,fr,en in NAV)}
  </ul>
  <a href="contact.html" class="btn" data-en="Contact us">Nous consulter</a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
</div></header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="flogo" src="/img/logo-tmi.png" alt="TMI" width="150" height="40">
        {T("Entreprise de travaux publics créée en 2023 : réseaux d'eau, voirie et enrobés, VRD, travaux spéciaux, bâtiment et génie civil.", "Public works company founded in 2023: water networks, roads and asphalt, utilities, special works, building and civil engineering.", 'p')}
      </div>
      <div>
        {T("L'entreprise", "The company", 'h4')}
        <ul>
          <li><a href="entreprise.html" data-en="Who we are">Qui sommes-nous</a></li>
          <li><a href="realisations.html" data-en="Projects">Réalisations</a></li>
          <li><a href="materiel.html" data-en="Equipment">Matériel</a></li>
          <li><a href="engagements.html" data-en="Commitments">Engagements</a></li>
          <li><a href="carrieres.html" data-en="Careers">Carrières</a></li>
        </ul>
      </div>
      <div>
        {T("Expertises", "Expertise", 'h4')}
        <ul>
          <li><a href="reseaux-eau-potable-assainissement-guadeloupe.html" data-en="Water networks">Réseaux humides</a></li>
          <li><a href="enrobes-voirie-guadeloupe-saint-martin.html" data-en="Roads and asphalt">Routes et enrobés</a></li>
          <li><a href="vrd-terrassement-guadeloupe.html" data-en="Utilities and earthworks">VRD et terrassement</a></li>
          <li><a href="fondations-speciales-parasismique-guadeloupe.html" data-en="Special works">Travaux spéciaux</a></li>
          <li><a href="batiment-genie-civil-guadeloupe.html" data-en="Building and civil engineering">Bâtiment et génie civil</a></li>
        </ul>
      </div>
      <div>
        {T("Contact", "Contact", 'h4')}
        <ul>
          <li>{ADDR_FR}</li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="contact.html" data-en="Contact form">Formulaire de contact</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span id="year">2026</span> TMI Travaux Modernes Ingénierie</span>
      <nav><a href="mentions-legales.html" data-en="Legal notice">Mentions légales</a><a href="contact.html">Contact</a></nav>
    </div>
  </div>
</footer>
<script src="/assets/site.js?v={JS_V}" defer></script>
</body>
</html>
'''

def phero(page_title_fr, page_title_en, lead_fr, lead_en, img, crumb_fr, crumb_en):
    return f'''<section class="phero">
  {pic(img, '', '', lazy=False, prio=True, sizes='100vw')}
  <div class="wrap">
    <p class="crumbs"><a href="index.html" data-en="Home">Accueil</a> / {T(crumb_fr, crumb_en)}</p>
    {T(page_title_fr, page_title_en, 'h1')}
    {T(lead_fr, lead_en, 'p', 'lead')}
  </div>
</section>
'''

# ---------------------------------------------------------------- Données
CD = ("Conseil départemental de la Guadeloupe", "Guadeloupe Departmental Council")
SM = ("Collectivité de Saint-Martin", "Collectivity of Saint-Martin")
VH = ("Commune de Vieux-Habitants", "Town of Vieux-Habitants")
SK = ("SIKOA", "SIKOA")
CATS = {'reseaux': ('Réseaux humides', 'Water networks'), 'voirie': ('Routes, VRD et urgences', 'Roads, utilities and emergency works'),
        'fondations': ('Travaux spéciaux', 'Special works'), 'batiment': ('Bâtiment et génie civil', 'Building and civil engineering')}
def D(n, u):
    fr = {'mois': 'mois', 'semaine': 'semaine' if n == 1 else 'semaines', 'jours': 'jours'}[u]
    en = {'mois': 'month' if n == 1 else 'months', 'semaine': 'week' if n == 1 else 'weeks', 'jours': 'days'}[u]
    return (f'{n} {fr}', f'{n} {en}')
REFS = [
 ('ref-petit-canal-aep','reseaux','AEP et assainissement, secteur Cornet','Water supply and sanitation, Cornet area','Petit-Canal',("SMGEAG","SMGEAG"),D(8,'mois'),6275044,
  "6 km de réseau d'adduction d'eau potable, 6 km de canalisation d'eaux usées et 450 branchements avec coffrets de comptage, pour améliorer la desserte en eau et la performance du réseau d'assainissement.",
  "6 km of drinking water mains, 6 km of sewer pipes and 450 connections with meter boxes, improving water supply and sewer network performance."),
 ('ref-bergevin-parasismique','fondations','Renforcement parasismique, résidence Bergevin','Seismic reinforcement, Bergevin residence','Pointe-à-Pitre',SK,D(12,'mois'),3376600,
  "Mise en œuvre de 384 micropieux et construction de voiles en béton armé en périphérie, sur environ 15 m de hauteur, pour renforcer la stabilité des ouvrages et leur conformité parasismique.",
  "384 micropiles and perimeter reinforced concrete walls about 15 m high, strengthening the buildings and bringing them to seismic standards."),
 ('ref-rue-de-hollande','voirie','Réfection de voirie, rue de Hollande','Road resurfacing, Rue de Hollande','Marigot, Saint-Martin',SM,D(1,'semaine'),680343,
  "Enrobé par intermittence, en pleine largeur et par bandes, sur environ 800 m, soit 600 tonnes mises en œuvre.",
  "Full-width and strip asphalt paving in phases over about 800 m, 600 tonnes laid."),
 ('ref-vieux-habitants-class','batiment','Réaménagement du CLASS','Refurbishment of the CLASS building','Vieux-Habitants',VH,D(5,'mois'),639289,
  "Réhabilitation comprenant la reprise de la toiture et l'intervention de l'ensemble des corps d'état, avec mise en conformité et amélioration des conditions d'accueil.",
  "Rehabilitation including roof renovation and all trades, with compliance upgrades and improved facilities."),
 ('ref-friars-bay','voirie',"Réfection de voirie, Friar's Bay","Road resurfacing, Friar's Bay",'Saint-Martin',SM,D(1,'semaine'),520678,
  "Enrobé en pleine largeur sur un axe principal d'environ 800 m, soit 500 tonnes, pour la sécurité et le confort des usagers.",
  "Full-width asphalt paving on a main road over about 800 m, 500 tonnes, for road user safety and comfort."),
 ('ref-vieux-fort-talus','fondations','Confortement de talus','Slope stabilisation','Vieux-Fort',CD,D(3,'mois'),411130,
  "60 m² de béton projeté et 450 m² de paroi clouée double treillis avec forages injectés, renforcement du mur existant, curage du cours d'eau et remise en état par enrochement.",
  "60 m² of shotcrete and 450 m² of double-mesh soil-nailed wall with grouted anchors, strengthening of the existing wall, stream clearing and riprap reinstatement."),
 ('ref-vieux-fort-amenagement','voirie','Aménagement et sécurisation','Development and road safety works','Vieux-Fort',CD,D(3,'mois'),408434,
  "Accotements en béton et trottoirs sur environ 400 m pour sécuriser les usagers, et réseau d'eaux pluviales pour la gestion du ruissellement.",
  "Concrete verges and pavements over about 400 m to protect road users, and a stormwater network to manage runoff."),
 ('ref-capesterre','voirie','Aménagement et voirie','Development and roadworks','Capesterre-Belle-Eau',CD,D(3,'mois'),347000,
  "Amélioration des accotements, réseau d'eaux pluviales DN 600 sur environ 200 m et réfection de la chaussée en enrobé sur le même linéaire.",
  "Verge improvements, a DN 600 stormwater pipe over about 200 m and asphalt resurfacing along the same stretch."),
 ('ref-colombier','voirie','Réfection de voirie, rue Colombier','Road resurfacing, Rue Colombier','Rambaud, Saint-Martin',SM,D(1,'semaine'),320986,
  "Intervention sur un axe principal : enrobé en pleine largeur sur deux voies, environ 315 m, soit 320 tonnes.",
  "Work on a main road: full-width paving on two lanes, about 315 m, 320 tonnes."),
 ('ref-gosier-fondations','fondations','Fondations spéciales, terrain de basket','Special foundations, basketball court','Belle-Plaine, Le Gosier',("Commune du Gosier","Town of Le Gosier"),D(2,'mois'),280000,
  "24 micropieux de 10 m et 24 massifs en béton armé destinés à supporter la future charpente métallique de couverture du terrain.",
  "24 micropiles 10 m deep and 24 reinforced concrete footings to carry the future steel roof over the court."),
 ('ref-vieux-habitants-creche','batiment','Reconstruction et réhabilitation de la crèche','Reconstruction and rehabilitation of the nursery','Vieux-Habitants',VH,D(5,'mois'),259124,
  "Réhabilitation lourde, gros œuvre et ensemble des corps d'état, pour une remise en service rapide et un accueil sécurisé des enfants.",
  "Heavy rehabilitation, structural work and all trades, for a quick return to service and safe care for children."),
 ('ref-soufriere-urgence','voirie',"Travaux d'urgence, La Soufrière",'Emergency works, La Soufrière','Saint-Claude',CD,D(2,'mois'),210250,
  "Intervention d'urgence après un éboulement consécutif à une tempête : terrassement, sécurisation des abords et caniveau bétonné d'environ 60 m.",
  "Emergency response to a storm-induced landslide: earthworks, securing the area and a concrete gutter about 60 m long."),
 ('ref-saint-martin-soutenement','fondations','Mur de soutènement, quartier Spring','Retaining wall, Spring district','Saint-Martin',SK,D(3,'mois'),193764,
  "Mur de soutènement d'environ 150 m sur 2 m de hauteur, pour la stabilité des terrains et la sécurisation des infrastructures.",
  "Retaining wall about 150 m long and 2 m high, stabilising the ground and protecting infrastructure."),
 ('ref-froston','voirie','Réfection de voirie, Froston','Road resurfacing, Froston','Saint-Martin',SM,D(3,'jours'),145677,
  "Reprise de la chaussée sur la place de l'église de Froston, avec 120 tonnes d'enrobé mises en œuvre.",
  "Resurfacing of the Froston church square, with 120 tonnes of asphalt laid."),
 ('ref-vieux-habitants-pont','voirie','Sécurisation du pont de Vanier','Vanier bridge safety works','Vieux-Habitants',CD,D(1,'semaine'),73450,
  "Travaux d'enrobé pour la sécurisation du pont de Vanier, environ 100 tonnes mises en œuvre.",
  "Asphalt works to make the Vanier bridge safer, about 100 tonnes laid."),
]

def fmt_ht(n):
    return fmt_eur(n) + (' excl. VAT' if LANG == 'en' else ' HT')
def fmt_eur(n):
    if LANG == 'en':
        return '€' + f"{n:,}"
    return f"{n:,}".replace(',', ' ') + ' €'

def card(r, as_button=True, link=None):
    img, cat, tfr, ten, place, moa, dur, amt, dfr, den = r
    cfr, cen = CATS[cat]
    data = (f' data-cat="{cat}" data-amt="{amt}" data-place="{a(place)}"'
            f' data-title-fr="{a(tfr)}" data-title-en="{a(ten)}" data-cat-fr="{a(cfr)}" data-cat-en="{a(cen)}"'
            f' data-desc-fr="{a(dfr)}" data-desc-en="{a(den)}" data-moa-fr="{a(moa[0])}" data-moa-en="{a(moa[1])}"'
            f' data-dur-fr="{a(dur[0])}" data-dur-en="{a(dur[1])}"')
    inner = (f'<div class="ph">{pic(img, tfr, ten, 1191, 653)}</div>'
             f'<div class="bd">{T(cfr, cen, "span", "cat")}{T(tfr, ten, "h3")}'
             f'<div class="meta">{T(moa[0], moa[1])}<span>{esc(place)}</span>{T(dur[0], dur[1])}<span class="amt">{fmt_eur(amt)}</span></div></div>')
    if link:
        return f'<a class="card" href="{link}"{data}>{inner}</a>'
    return f'<button type="button" class="card"{data}>{inner}</button>'


# ---------------------------------------------------------------- Chantiers 2026 (sans photo : illustration par métier)
def motif(kind):
    W, H = 400, 250
    bg = '#001746'; b = '#0099DD'; w = 'rgba(255,255,255,.55)'; f = 'rgba(255,255,255,.12)'
    g = ''
    if kind == 'reseaux':
        g += f'<rect x="0" y="0" width="{W}" height="95" fill="#0A2A63"/>'
        g += ''.join(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{f}" stroke-width="1"/>' for y in range(110, 250, 14))
        g += f'<circle cx="150" cy="165" r="46" fill="none" stroke="{b}" stroke-width="10"/><circle cx="150" cy="165" r="30" fill="{b}" opacity=".25"/>'
        g += f'<circle cx="275" cy="175" r="30" fill="none" stroke="{w}" stroke-width="7"/>'
        g += f'<path d="M60 95 L60 250 M340 95 L340 250" stroke="{w}" stroke-width="2" stroke-dasharray="6 6"/>'
    elif kind == 'voirie':
        layers = [(70, 26, '#1B1F24'), (96, 30, '#2A3A5A'), (126, 40, '#0A2A63'), (166, 84, '#06204F')]
        for y, h, c in layers:
            g += f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="{c}"/>'
        g += f'<line x1="0" x2="{W}" y1="70" y2="70" stroke="{b}" stroke-width="6"/>'
        g += ''.join(f'<rect x="{x}" y="80" width="34" height="5" fill="{w}"/>' for x in range(10, W, 64))
        g += ''.join(f'<circle cx="{(i*53)%W}" cy="{140+(i*17)%22}" r="3" fill="{f}"/>' for i in range(1, 28))
    elif kind == 'fondations':
        g += f'<rect x="0" y="0" width="{W}" height="80" fill="#0A2A63"/><rect x="60" y="40" width="280" height="40" fill="{w}" opacity=".35"/>'
        g += ''.join(f'<line x1="{x}" x2="{x}" y1="80" y2="235" stroke="{b}" stroke-width="7"/>' for x in (95, 160, 240, 305))
        g += ''.join(f'<line x1="0" x2="{W}" y1="{y}" y2="{y-30}" stroke="{f}" stroke-width="1.5"/>' for y in range(110, 300, 18))
    else:  # batiment
        g += f'<rect x="0" y="210" width="{W}" height="40" fill="#0A2A63"/>'
        for i, (x, wd, h) in enumerate([(70, 120, 150), (200, 140, 110)]):
            g += f'<rect x="{x}" y="{210-h}" width="{wd}" height="{h}" fill="none" stroke="{w}" stroke-width="3"/>'
            g += ''.join(f'<rect x="{x+12+c*30}" y="{210-h+14+r*32}" width="18" height="18" fill="{b if (r+c+i)%3==0 else f}"/>' for r in range(h//32 - 1) for c in range(wd//30))
        g += f'<polygon points="200,100 270,60 340,100" fill="none" stroke="{b}" stroke-width="4"/>'
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{bg}"/>{g}</svg>'

ST_EC = ('En cours', 'In progress'); ST_LV = ('Livré en 2026', 'Delivered in 2026')
PUB_PORT = ("Grand Port Maritime de la Guadeloupe (GPMG)", "Guadeloupe Port Authority (GPMG)"); PUB_EAU = ("Établissement public de l'eau", "Public water utility")
BAILLEUR = ("Bailleur social", "Social landlord"); COMMUNE = ("Commune", "Town council"); SPL = ("Société publique d'aménagement", "Public development company")
COLL = ("Collectivité", "Local authority")
GP, SXM = "Guadeloupe", "Saint-Martin"
# (catégorie, statut, titre fr, titre en, maître d'ouvrage, territoire, photo ou None, légende photo fr/en)
CURRENT = [
 ('reseaux', ST_EC, "Reprise de l'adduction d'eau potable du quai 6", "Drinking water supply renewal, Quay 6", PUB_PORT, GP, '2026-quai-aep', ("Quai en cours d'équipement", "Quay being equipped")),
 ('fondations', ST_EC, "Confortement parasismique de la résidence Legitimus", "Seismic strengthening of the Legitimus residence", SK, GP, '2026-residence-parasismique', ("État avant travaux", "Before works")),
 ('fondations', ST_EC, "Démolition, gros œuvre et fondations spéciales : 206 logements de Rivière Salée", "Demolition, structural work and special foundations: 206 homes in Rivière Salée", SK, "Pointe-à-Pitre", None, None),
 ('reseaux', ST_EC, "Renouvellement d'eau potable et création d'un réseau d'eaux usées", "Water main renewal and new sewer network", PUB_EAU, SXM, None, None),
 ('reseaux', ST_EC, "Travaux de renouvellement du réseau AEP de Sainte-Anne, impasse Vallier", "Drinking water network renewal in Sainte-Anne, Impasse Vallier", CD, GP, None, None),
 ('reseaux', ST_EC, "Travaux de renouvellement du réseau AEP de Saint-François, tranche 1 : secteurs de Bragelogne et Saint-Charles", "Drinking water network renewal in Saint-François, phase 1: Bragelogne and Saint-Charles areas", CD, GP, None, None),
 ('voirie', ST_EC, "Réfection en enrobé multisite du port", "Multi-site asphalt resurfacing of the port", PUB_PORT, GP, None, None),
 ('voirie', ST_EC, "Voirie et réseaux divers du quai 12", "Roads and utilities, Quay 12", PUB_PORT, GP, None, None),
 ('voirie', ST_EC, "Aménagement d'un secteur : terrassement, voirie, réseaux", "Area development: earthworks, roads, networks", SPL, GP, None, None),
 ('voirie', ST_EC, "Voirie et réseaux divers de la résidence Legitimus", "Roads and utilities for the Legitimus residence", SK, GP, None, None),
 ('batiment', ST_EC, "Construction d'un bâtiment public", "Construction of a public building", ("Ville du Moule", "Town of Le Moule"), GP, None, None),
 ('batiment', ST_EC, "Hangar d'un centre technique municipal", "Municipal technical centre shed", ("Commune d'Anse-Bertrand", "Town of Anse-Bertrand"), GP, None, None),
 ('voirie', ST_EC, "Création d'une aire de covoiturage", "New car-sharing park-and-ride", VH, GP, None, None),
 ('reseaux', ST_EC, "Forages pour la ressource en eau potable", "Boreholes for drinking water supply", PUB_EAU, GP, None, None),
 ('voirie', ST_LV, "Réfection en enrobé de la route de Friar's Bay, phase 2", "Asphalt resurfacing of Friar's Bay road, phase 2", SM, "Saint-Martin", None, None),
 ('voirie', ST_LV, "Reprises de chaussée en enrobé, route de Bellevue", "Asphalt road repairs, Bellevue road", SM, "Saint-Martin", None, None),
 ('voirie', ST_LV, "Réfection en enrobé du carrefour de Pic Paradis", "Asphalt resurfacing of the Pic Paradis junction", SM, "Saint-Martin", None, None),
 ('voirie', ST_LV, "Réfection de voirie en centre-ville", "Town-centre road resurfacing", SM, SXM, None, None),
]

AMOUNTS = {"Reprise de l'adduction d'eau potable du quai 6": 145900, "Confortement parasismique de la résidence Legitimus": 597740, "Renouvellement d'eau potable et création d'un réseau d'eaux usées": 886557, 'Travaux de renouvellement du réseau AEP de Sainte-Anne, impasse Vallier': 195971, 'Travaux de renouvellement du réseau AEP de Saint-François, tranche 1 : secteurs de Bragelogne et Saint-Charles': 620268, 'Réfection en enrobé multisite du port': 361950, "Aménagement d'un secteur : terrassement, voirie, réseaux": 277320, "Voirie et réseaux divers de la résidence Legitimus": 69861, "Construction d'un bâtiment public": 92577, "Hangar d'un centre technique municipal": 203910, 'Réfection de voirie en centre-ville': 198627, "Voirie et réseaux divers du quai 12": 507125, "Création d'une aire de covoiturage": 600656, "Forages pour la ressource en eau potable": 897195, "Démolition, gros œuvre et fondations spéciales : 206 logements de Rivière Salée": 4970359, "Réfection en enrobé de la route de Friar's Bay, phase 2": 625903, "Reprises de chaussée en enrobé, route de Bellevue": 461123, "Réfection en enrobé du carrefour de Pic Paradis": 70557}

def ccard(c):
    cat, st, tfr, ten, moa, terr, img, cap = c
    cfr, cen = CATS[cat]
    live = ' live' if st is ST_EC else ''
    return (f'<article class="ccard"><div class="cvis">{pic(img, tfr, ten, 1400, 875)}'
            f'<span class="status{live}" data-en="{a(st[1])}">{esc(st[0])}</span>'
            f'<span class="ccap" data-en="{a(cap[1])}">{esc(cap[0])}</span></div>'
            f'<div class="bd">{T(cfr, cen, "span", "cat")}{T(tfr, ten, "h3")}'
            f'<div class="meta">{T(moa[0], moa[1])}<span>{terr}</span>'
            + (f'<span class="amt">{fmt_ht(AMOUNTS[tfr])}</span>' if tfr in AMOUNTS else '') + '</div></div></article>')

def crow(c, link=None):
    cat, st, tfr, ten, moa, terr, *_ = c
    cfr, cen = CATS[cat]
    live = ' live' if st is ST_EC else ''
    ttl = f'<strong><a href="{link}" data-en="{a(ten)}">{esc(tfr)}</a></strong>' if link else T(tfr, ten, "strong")
    return (f'<li class="crow">{T(cfr, cen, "span", "cat")}{ttl}{T(moa[0], moa[1], "span", "moa")}'
            f'<span class="terr">{terr}</span><span class="amt">{fmt_ht(AMOUNTS[tfr]) if tfr in AMOUNTS else ""}</span><span class="st{live}" data-en="{a(st[1])}">{esc(st[0])}</span></li>')

SLUGS = {'reseaux': 'reseaux-eau-potable-assainissement-guadeloupe.html', 'routes': 'enrobes-voirie-guadeloupe-saint-martin.html',
         'vrd': 'vrd-terrassement-guadeloupe.html', 'speciaux': 'fondations-speciales-parasismique-guadeloupe.html',
         'batiment': 'batiment-genie-civil-guadeloupe.html'}

# ---------------------------------------------------------------- Accueil
METIERS = [
 ('reseaux','ref-petit-canal-aep','Réseaux humides','Water networks',
  "Adduction d'eau potable, eaux usées et pluviales, branchements et ouvrages annexes.",
  "Drinking water supply, wastewater and stormwater networks, connections and ancillary structures."),
 ('routes','ref-colombier','Routes et enrobés','Roads and asphalt',
  "Rabotage, mise en œuvre et compactage d'enrobés, de jour comme de nuit, avec notre propre atelier.",
  "Milling, paving and compaction, day or night, with our own asphalt crew and plant."),
 ('vrd','ref-vieux-fort-amenagement','VRD et terrassement','Utilities and earthworks',
  "Voirie, réseaux divers, trottoirs, accotements et aménagement des espaces publics.",
  "Roads, utilities, pavements, verges and public space development."),
 ('speciaux','ref-gosier-fondations','Travaux spéciaux','Special works',
  "Micropieux, parois clouées, soutènements, béton projeté et renforcement parasismique.",
  "Micropiles, soil-nailed walls, retaining structures, shotcrete and seismic reinforcement."),
 ('batiment','ref-vieux-habitants-class','Bâtiment et génie civil','Building and civil engineering',
  "Réhabilitation, reconstruction, gros œuvre et béton armé pour les équipements publics et le logement.",
  "Rehabilitation, reconstruction, structural work and reinforced concrete for public facilities and housing."),
]

def page_index():
    n_ec = sum(1 for c in CURRENT if c[1] is ST_EC)
    h = head('index.html', "TMI Travaux Modernes Ingénierie | Travaux publics en Guadeloupe et à Saint-Martin",
             "TMI réalise les réseaux d'eau, la voirie et les enrobés, les VRD, les travaux spéciaux et le génie civil des collectivités et maîtres d'ouvrage de Guadeloupe et de Saint-Martin.",
             title_en='TMI Travaux Modernes Ingénierie | Public works in Guadeloupe and Saint-Martin', desc_en='TMI builds water networks, roads and asphalt, utilities, special foundations and civil engineering works for public authorities and clients in Guadeloupe and Saint-Martin.')
    metiers = ''.join(
        f'<a class="metier" href="{SLUGS[mid]}">{pic(img, "", "")}<div class="in">{T(fr, en, "h3")}{T(dfr, den, "p")}'
        f'{T("Découvrir le métier", "Explore", "span", "go")}</div></a>' for mid, img, fr, en, dfr, den in METIERS)
    feat = ''.join(card(r, link='realisations.html') for r in REFS[:3])
    body = f'''<section class="hero">
  {pic('ref-colombier', "Mise en œuvre d'enrobés de nuit, rue Colombier à Saint-Martin", "Night-time paving, Rue Colombier, Saint-Martin", lazy=False, prio=True, sizes='100vw')}
  <div class="wrap">
    {T("Les infrastructures de nos îles, construites ici.", "Island infrastructure, built here.", 'h1')}
    {T("TMI réalise les réseaux d'eau, les routes, les fondations spéciales et les ouvrages de génie civil des collectivités et maîtres d'ouvrage de Guadeloupe et de Saint-Martin, avec ses propres équipes et son propre matériel.", "TMI builds water networks, roads, special foundations and civil engineering works for local authorities and clients in Guadeloupe and Saint-Martin, with its own teams and its own equipment.", 'p', 'lead')}
    <div class="actions">
      <a class="btn" href="realisations.html" data-en="See our projects">Voir nos réalisations</a>
      <a class="btn line light" href="contact.html" data-en="Discuss a project">Parler d'un projet</a>
    </div>
  </div>
</section>

<section class="figures-band"><div class="wrap">
  <dl class="figures">
    <div><dd>10 M€</dd>{T("de chiffre d'affaires en 2025, et autant en 2026", "revenue in 2025, and the same again in 2026", 'dt')}</div>
    <div><dd>{n_ec}</dd>{T("chantiers en cours en Guadeloupe et à Saint-Martin", "projects under way in Guadeloupe and Saint-Martin", 'dt')}</div>
    <div><dd>50+</dd>{T("engins et véhicules en propre, entretenus par nos équipes", "machines and vehicles owned and maintained in-house", 'dt')}</div>
    <div><dd>30+</dd>{T("chantiers par an pour des maîtres d'ouvrage publics et privés", "projects a year for public and private clients", 'dt')}</div>
  </dl>
</div></section>

<section class="now"><div class="wrap">
  <div class="now-head">{T("En ce moment", "Right now", 'p', 'kicker')}<a class="link" href="realisations.html#2026" data-en="All 2026 projects">Tous les chantiers 2026</a></div>
  <ul class="now-list">{''.join(f'<li><span class="dot"></span><div>{T(c[2], c[3], "strong")}<span>{T(c[4][0], c[4][1])}, {esc(c[5])}</span></div></li>' for c in CURRENT[:4])}</ul>
</div></section>

<section class="sect"><div class="wrap">
  <div class="sect-head">
    <div>{T("Nos métiers", "What we do", 'p', 'kicker')}{T("Cinq métiers, une même organisation de chantier", "Five trades, one site organisation", 'h2')}</div>
    {T("De la tranchée à la couche de roulement, du micropieu à la toiture : nous réalisons chaque étape avec nos conducteurs de travaux, nos chefs de chantier et notre parc.", "From trench to road surface, from micropile to roof: every stage is carried out by our own site managers, foremen and fleet.", 'p', 'lead')}
  </div>
  <div class="metiers">{metiers}</div>
</div></section>

<section class="sect tint"><div class="wrap">
  <div class="sect-head">
    <div>{T("Réalisations", "Projects", 'p', 'kicker')}{T("Nos chantiers les plus importants de 2025", "Our largest projects in 2025", 'h2')}</div>
    <div>{T("Quinze opérations livrées en 2025, de 73 000 € à 6,3 M€, pour le Département, la Collectivité de Saint-Martin, le SMGEAG, SIKOA et plusieurs communes.", "Fifteen projects delivered in 2025, from €73k to €6.3m, for the Department, the Collectivity of Saint-Martin, SMGEAG, SIKOA and several towns.", 'p', 'lead')}
    <p style="margin-top:1.2rem"><a class="link" href="realisations.html" data-en="All projects">Toutes les réalisations</a></p></div>
  </div>
  <div class="cards">{feat}</div>
</div></section>

<section class="sect"><div class="wrap quote-block">
  <figure class="portrait" style="margin:0">
    {pic('johane-devouton', 'Johane Devouton, Présidente de TMI', 'Johane Devouton, President of TMI', sizes='(max-width:900px) 100vw, 420px')}
    <figcaption><strong>Johane Devouton</strong>{T("Présidente", "President")}</figcaption>
  </figure>
  <blockquote>
    {T("Le mot de la Présidente", "A word from our President", 'p', 'kicker')}
    {T("« Nous avons voulu bâtir bien plus qu'une entreprise de BTP : une équipe soudée, ancrée dans nos îles, qui construit durablement pour celles et ceux qui y vivent. »", "“We set out to build far more than a construction company: a close-knit team, rooted in our islands, building to last for the people who live here.”", 'p', 'q')}
    <footer><a class="link" href="entreprise.html#presidente" data-en="Read the full message">Lire le message</a></footer>
  </blockquote>
</div></section>

<section class="sect dark on-dark"><div class="wrap">
  <div class="sect-head">
    <div>{T("Engagements", "Commitments", 'p', 'kicker')}{T("Sécurité, qualité, environnement, délais", "Safety, quality, environment, deadlines", 'h2')}</div>
    {T("Ce sont nos priorités sur chaque chantier. Elles reposent sur la formation continue de nos équipes et sur un matériel que nous maîtrisons.", "These are our priorities on every site. They rest on continuous training for our teams and on equipment we control.", 'p', 'lead')}
  </div>
  <div class="pillars">
    <div class="pillar">{T("Sécurité", "Safety", 'h3')}{T("Sauveteurs secouristes du travail, AIPR, travaux en hauteur, signalisation temporaire et EPI complets.", "First-aid at work, utility proximity (AIPR) certification, work at height, temporary signage and full PPE.", 'p')}</div>
    <div class="pillar">{T("Qualité", "Quality", 'h3')}{T("Encadrement technique sur chaque opération et respect des délais, y compris en intervention d'urgence.", "Technical supervision on every project and deadlines met, including emergency works.", 'p')}</div>
    <div class="pillar">{T("Environnement", "Environment", 'h3')}{T("Chantiers propres, gestion des eaux de ruissellement et prévention des dommages aux réseaux existants.", "Clean sites, runoff management and prevention of damage to existing networks.", 'p')}</div>
    <div class="pillar">{T("Territoire", "Local roots", 'h3')}{T("Une entreprise guadeloupéenne qui investit dans les compétences locales et l'insertion.", "A Guadeloupe company investing in local skills and employment.", 'p')}</div>
  </div>
  <p style="margin-top:3rem"><a class="link" href="engagements.html" data-en="Our commitments">Nos engagements</a></p>
</div></section>

<section class="band on-dark"><div class="wrap">
  <div class="txt">
    {T("Carrières", "Careers", 'p', 'kicker')}
    {T("Construisez avec nous les ouvrages de demain", "Build tomorrow's infrastructure with us", 'h2')}
    {T("Conducteurs de travaux, chefs de chantier, chefs d'équipe, conducteurs d'engins, canalisateurs, compagnons : TMI grandit et cherche des talents en Guadeloupe et à Saint-Martin.", "Site managers, foremen, team leaders, machine operators, pipe layers, skilled workers: TMI is growing and looking for talent in Guadeloupe and Saint-Martin.", 'p', 'lead')}
    <div class="actions" style="margin-top:2rem"><a class="btn" href="carrieres.html" data-en="Apply">Postuler</a></div>
  </div>
  <div class="img">{pic('ouvrier-enrobe-nb', "Compagnon TMI lors d'un chantier d'enrobés", "TMI worker on an asphalt site", sizes='(max-width:900px) 100vw, 543px')}</div>
</div></section>

<section class="sect"><div class="wrap cta-row">
  {T("Un projet de travaux publics ou de génie civil ?", "A public works or civil engineering project?", 'h2')}
  <div class="actions"><a class="btn" href="contact.html" data-en="Contact us">Nous consulter</a><a class="btn line" href="expertises.html" data-en="Our expertise">Nos expertises</a></div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Entreprise
def page_entreprise():
    h = head('entreprise.html', "L'entreprise | TMI Travaux Modernes Ingénierie",
             "Créée en 2023 et dirigée par Johane Devouton, TMI est une entreprise de travaux publics guadeloupéenne : histoire, chiffres, valeurs et organisation.",
             title_en='The company | TMI Travaux Modernes Ingénierie', desc_en='Founded in 2023 and led by Johane Devouton, TMI is a public works contractor based in Guadeloupe: history, key figures, values and organisation.')
    body = phero("L'exigence des grands chantiers, l'ancrage du territoire", "Major-project standards, local roots",
                 "Créée en 2023 à Petit-Bourg et dirigée par Johane Devouton, TMI s'appuie sur plus de 15 ans d'expérience cumulée de ses équipes dans les travaux publics.",
                 "Founded in 2023 in Petit-Bourg and led by Johane Devouton, TMI draws on more than 15 years of combined public works experience.",
                 'ref-bergevin-parasismique', "L'entreprise", "Company")
    body += f'''
<section class="sect"><div class="wrap split top">
  <div>
    {T("Qui sommes-nous", "Who we are", 'p', 'kicker')}
    {T("Cinq métiers, une seule exigence", "Five trades, one standard", 'h2')}
  </div>
  <div class="prose">
    {T("TMI intervient en réseaux humides, travaux routiers, VRD et terrassement, enrobés, travaux spéciaux (fondations spéciales, soutènements, confortement de talus et parasismique), bâtiment et génie civil.", "TMI works in water networks, roadworks, utilities and earthworks, asphalt, special works (special foundations, retaining structures, slope stabilisation and seismic reinforcement), building and civil engineering.", 'p')}
    {T("Depuis sa création, l'entreprise organise ses activités et développe ses moyens techniques et humains pour gagner en performance et en qualité. Ses compétences techniques, administratives et financières lui permettent de répondre aux marchés publics comme aux opérations privées.", "Since its creation, the company has built up its technical and human resources to improve performance and quality. Its technical, administrative and financial capabilities allow it to take on public contracts and private projects alike.", 'p')}
    {T("La sécurité, la propreté, la qualité, la gestion de l'environnement et le respect des délais sont nos priorités sur l'ensemble de nos chantiers.", "Safety, cleanliness, quality, environmental management and meeting deadlines are our priorities on every site.", 'p')}
  </div>
</div></section>

<section class="sect tint"><div class="wrap">
  <div class="sect-head">
    <div>{T("Notre trajectoire", "Our growth", 'p', 'kicker')}{T("Une croissance continue depuis 2023", "Steady growth since 2023", 'h2')}</div>
    {T("Chiffre d'affaires annuel.", "Annual revenue.", 'p', 'lead')}
  </div>
  <ol class="timeline">
    <li><span class="y">2023</span><span class="v">1,03 M€</span>{T("Création de TMI à Petit-Bourg, premiers marchés de réseaux et de voirie.", "TMI founded in Petit-Bourg; first network and road contracts.", 'p')}</li>
    <li><span class="y">2024</span><span class="v">1,18 M€</span>{T("Constitution du parc matériel et de l'équipe d'encadrement.", "Equipment fleet and supervisory team put in place.", 'p')}</li>
    <li><span class="y">2025</span><span class="v">10 M€</span>{T("Changement d'échelle : 6,3 M€ d'AEP à Petit-Canal, parasismique à Bergevin, enrobés à Saint-Martin.", "A step change: €6.3m water network in Petit-Canal, seismic works at Bergevin, paving in Saint-Martin.", 'p')}</li>
    <li class="forecast"><span class="y">2026</span><span class="v">10 M€</span>{T("Consolidation : le port, les réseaux d'eau de Saint-Martin, l'aménagement, les enrobés en Guadeloupe et à Saint-Martin, et le parasismique avec SIKOA en Guadeloupe.", "Consolidation: port works, Saint-Martin water networks, developments, asphalt paving in Guadeloupe and Saint-Martin, and seismic works with SIKOA in Guadeloupe.", 'p')}</li>
  </ol>
</div></section>

<section class="sect"><div class="wrap split top">
  <div>
    {T("Répartition de l'activité", "Activity breakdown", 'p', 'kicker')}
    {T("Un portefeuille équilibré entre nos métiers", "A balanced portfolio across our trades", 'h2')}
    {T("Part du chiffre d'affaires par activité.", "Share of revenue by activity.", 'p', 'lead')}
  </div>
  <div class="bars">
    <div class="bar"><div class="lbl">{T("Réseaux humides", "Water networks")}<span>30 %</span></div><div class="track"><div class="fill" style="width:30%"></div></div></div>
    <div class="bar"><div class="lbl">{T("Travaux routiers, VRD, terrassement, enrobés", "Roadworks, utilities, earthworks, asphalt")}<span>28 %</span></div><div class="track"><div class="fill" style="width:28%"></div></div></div>
    <div class="bar"><div class="lbl">{T("Travaux spéciaux", "Special works")}<span>27 %</span></div><div class="track"><div class="fill" style="width:27%"></div></div></div>
    <div class="bar"><div class="lbl">{T("Bâtiment et génie civil", "Building and civil engineering")}<span>15 %</span></div><div class="track"><div class="fill" style="width:15%"></div></div></div>
  </div>
</div></section>

<section class="sect dark on-dark"><div class="wrap">
  <div class="sect-head">
    <div>{T("Notre identité", "Our identity", 'p', 'kicker')}{T("Mission, vision, valeurs", "Mission, vision, values", 'h2')}</div>
  </div>
  <div class="mvv">
    <div>{T("Notre mission", "Our mission", 'h3')}{T("Réaliser des projets qui répondent aux besoins de nos clients, en contribuant au développement des îles de la Caraïbe et à l'insertion sociale.", "Deliver projects that meet our clients' needs, while contributing to the development of the Caribbean islands and to social inclusion.", 'p')}</div>
    <div>{T("Notre vision", "Our vision", 'h3')}{T("Faire de notre organisation une plateforme qui investit dans le développement des compétences locales.", "Make our organisation a platform that invests in developing local skills.", 'p')}</div>
    <div>{T("Nos valeurs", "Our values", 'h3')}<div class="values">{T("Engagement", "Commitment")}{T("Rigueur", "Rigour")}{T("Excellence", "Excellence")}</div></div>
  </div>
</div></section>

<section class="sect" id="presidente"><div class="wrap quote-block">
  <figure class="portrait" style="margin:0">
    {pic('johane-devouton', 'Johane Devouton, Présidente de TMI', 'Johane Devouton, President of TMI', sizes='(max-width:900px) 100vw, 420px')}
    <figcaption><strong>Johane Devouton</strong>{T("Présidente", "President")}</figcaption>
  </figure>
  <div class="letter">
    {T("Le mot de la Présidente", "A word from our President", 'p', 'kicker')}
    {T("Chers collaborateurs et partenaires,", "Dear colleagues and partners,", 'p')}
    {T("En créant Travaux Modernes Ingénierie, nous avons voulu bâtir bien plus qu'une entreprise de BTP : réunir des femmes et des hommes qui partagent des valeurs fortes, le respect, l'exigence, la qualité, l'écoute et le sens des responsabilités.", "In creating Travaux Modernes Ingénierie, we set out to build far more than a construction company: to bring together women and men who share strong values of respect, high standards, quality, listening and responsibility.", 'p')}
    {T("Nous sommes une équipe soudée, ancrée en Guadeloupe, en Martinique et à Saint-Martin, portée par une même ambition : construire durablement, en valorisant nos îles, l'environnement et les projets de celles et ceux qui y vivent.", "We are a close-knit team, rooted in Guadeloupe, Martinique and Saint-Martin, driven by one ambition: to build to last, in a way that values our islands, the environment and the projects of the people who live here.", 'p')}
    {T("Depuis 2023, nous avançons avec sérieux et passion pour faire émerger des chantiers solides, utiles et porteurs de sens. Nos savoir-faire techniques sont là, nos moyens humains et matériels aussi. Ce qui fait la différence, c'est notre engagement collectif.", "Since 2023, we have moved forward with seriousness and passion to deliver projects that are solid, useful and meaningful. Our technical skills are in place, and so are our people and equipment. What makes the difference is our collective commitment.", 'p')}
    {T("TMI est jeune et déjà prête à relever de grands défis. Le plus beau reste à venir, et nous avons hâte de le construire à vos côtés.", "TMI is young and already ready for major challenges. The best is yet to come, and we look forward to building it with you.", 'p')}
    <p class="sign">Johane Devouton</p>
  </div>
</div></section>

<section class="sect tint"><div class="wrap">
  <div class="sect-head">
    <div>{T("Organisation", "Organisation", 'p', 'kicker')}{T("Une direction resserrée, un encadrement de terrain", "A lean management team, hands-on site supervision", 'h2')}</div>
    {T("Chaque opération est suivie par un conducteur de travaux et un chef de chantier spécialisés dans le métier concerné.", "Every project is run by a site manager and a foreman specialised in the trade concerned.", 'p', 'lead')}
  </div>
  <div class="people" style="grid-template-columns:repeat(2,minmax(0,1fr))">
    <div class="person"><strong>Johane Devouton</strong>{T("Présidente", "President")}</div>
    <div class="person"><strong>Arnaud Disson</strong>{T("Directeur technique", "Technical Director")}</div>
  </div>
  <div class="teamline">
    <div><b>4</b>{T("conducteurs de travaux : travaux spéciaux, VRD et génie civil, génie civil, VRD et enrobés", "site managers: special works, utilities and civil engineering, civil engineering, roads and asphalt")}</div>
    <div><b>4</b>{T("chefs de chantier : travaux spéciaux, AEP et assainissement, génie civil, VRD et enrobés", "foremen: special works, water and sanitation, civil engineering, roads and asphalt")}</div>
    <div><b>2</b>{T("assistantes de direction et de conduite de travaux", "management and site administration assistants")}</div>
  </div>
</div></section>

<section class="sect"><div class="wrap">
  <div class="sect-head">
    <div>{T("Ils nous font confiance", "They trust us", 'p', 'kicker')}{T("Nos maîtres d'ouvrage", "Our clients", 'h2')}</div>
  </div>
  <ul class="clients">
    <li data-en="Guadeloupe Departmental Council">Conseil départemental de la Guadeloupe</li>
    <li data-en="Collectivity of Saint-Martin">Collectivité de Saint-Martin</li>
    <li data-en="Guadeloupe Regional Council">Conseil régional de la Guadeloupe</li>
    <li>SMGEAG</li>
    <li>SIKOA</li>
    <li data-en="Town of Le Gosier">Commune du Gosier</li>
    <li data-en="Town of Vieux-Habitants">Commune de Vieux-Habitants</li>
  </ul>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Expertises
EXPERTISES = [
 ('reseaux', 'ref-petit-canal-aep', 'Réseaux humides', 'Water networks',
  "Nous posons et renouvelons les réseaux d'adduction et de distribution d'eau potable, les réseaux d'eaux usées et d'eaux pluviales, avec les branchements particuliers, les ouvrages annexes et la réfection de chaussée qui les accompagnent.",
  "We lay and renew drinking water supply and distribution networks, wastewater and stormwater networks, with the associated household connections, ancillary structures and road reinstatement.",
  [("Adduction et distribution d'eau potable", "Drinking water supply and distribution"), ("Réseaux d'eaux usées", "Wastewater networks"), ("Réseaux d'eaux pluviales", "Stormwater networks"), ("Branchements et coffrets de comptage", "Connections and meter boxes"), ("Ouvrages annexes", "Ancillary structures"), ("Essais et mise en eau", "Pressure testing and commissioning")],
  "Lasers de canalisation, niveaux optiques, détecteurs de réseaux, pompes d'exhaure, pelles 6 à 16 t.", "Pipe lasers, optical levels, utility detectors, dewatering pumps, 6 to 16 t excavators.",
  "AEP et assainissement du secteur Cornet à Petit-Canal (6,3 M€).", "Cornet water supply and sanitation, Petit-Canal (€6.3m)."),
 ('routes', 'ref-rue-de-hollande', 'Routes et enrobés', 'Roads and asphalt',
  "Notre atelier d'enrobés intégré couvre le rabotage, la mise en œuvre au finisseur grande ou petite largeur et le compactage. Nous intervenons de nuit lorsque la circulation l'impose, sur les axes principaux comme sur les voies communales.",
  "Our in-house asphalt crew handles milling, paving with wide or narrow pavers and compaction. We work at night when traffic requires it, on main roads and local streets alike.",
  [("Rabotage", "Milling"), ("Enrobés en pleine largeur et par bandes", "Full-width and strip paving"), ("Compactage", "Compaction"), ("Couches d'accrochage", "Tack coats"), ("Travail de nuit", "Night work"), ("Parkings et voies de circulation", "Car parks and roadways")],
  "2 raboteuses XCMG (1,00 et 1,50 m), 2 finisseurs XCMG (0,50 à 7,50 m), 5 compacteurs, bouille à émulsion 2 000 L.", "2 XCMG milling machines (1.00 and 1.50 m), 2 XCMG pavers (0.50 to 7.50 m), 5 rollers, 2,000 L emulsion sprayer.",
  "Rue de Hollande, Friar's Bay, rue Colombier et Froston à Saint-Martin.", "Rue de Hollande, Friar's Bay, Rue Colombier and Froston in Saint-Martin."),
 ('vrd', 'ref-vieux-fort-amenagement', 'VRD et terrassement', 'Utilities and earthworks',
  "Voiries et réseaux divers, terrassement, trottoirs, accotements, réseaux pluviaux : nous aménageons et sécurisons les espaces publics, en lien avec les collectivités et les aménageurs.",
  "Roads and utilities, earthworks, pavements, verges, stormwater networks: we develop and secure public spaces with local authorities and developers.",
  [("Terrassement", "Earthworks"), ("Voirie et trottoirs", "Roads and pavements"), ("Accotements béton", "Concrete verges"), ("Réseaux pluviaux", "Stormwater drainage"), ("Sécurisation des usagers", "Road user safety"), ("Aménagements urbains", "Urban development")],
  "8 mini-pelles, pelles 6 à 15 t, 2 pelles sur pneus 16 t, 2 tractopelles, 7 camions bennes.", "8 mini excavators, 6 to 15 t excavators, 2 wheeled excavators 16 t, 2 backhoe loaders, 7 dump trucks.",
  "Aménagements à Vieux-Fort et Capesterre-Belle-Eau pour le Département.", "Developments in Vieux-Fort and Capesterre-Belle-Eau for the Department."),
 ('speciaux', 'ref-bergevin-parasismique', 'Travaux spéciaux', 'Special works',
  "En zone sismique, la nature du terrain impose souvent des solutions particulières. Nous réalisons micropieux, parois clouées, soutènements, béton projeté et renforcement parasismique de bâtiments existants, ainsi que les confortements de talus.",
  "In a seismic zone, ground conditions often call for special solutions. We build micropiles, soil-nailed walls, retaining structures, shotcrete and seismic reinforcement of existing buildings, as well as slope stabilisation.",
  [("Micropieux", "Micropiles"), ("Parois clouées", "Soil-nailed walls"), ("Murs de soutènement", "Retaining walls"), ("Béton projeté", "Shotcrete"), ("Renforcement parasismique", "Seismic reinforcement"), ("Confortement de talus", "Slope stabilisation")],
  "Foreuses Comacchio MC8 HT et XCMG XLS4, ensembles Marini, centrale d'injection, unités de gunitage, compresseurs jusqu'à 24 m³.", "Comacchio MC8 HT and XCMG XLS4 rigs, Marini drilling units, grouting plant, shotcrete units, compressors up to 24 m³.",
  "384 micropieux à la résidence Bergevin, paroi clouée à Vieux-Fort, micropieux au Gosier.", "384 micropiles at the Bergevin residence, soil-nailed wall in Vieux-Fort, micropiles in Le Gosier."),
 ('batiment', 'ref-vieux-habitants-creche', 'Bâtiment et génie civil', 'Building and civil engineering',
  "Réhabilitation lourde, reconstruction, gros œuvre et structures en béton armé : nous intervenons sur les équipements publics, les logements collectifs et les bâtiments industriels, en coordonnant l'ensemble des corps d'état.",
  "Heavy rehabilitation, reconstruction, structural work and reinforced concrete: we work on public facilities, multi-unit housing and industrial buildings, coordinating all trades.",
  [("Gros œuvre", "Structural work"), ("Béton armé", "Reinforced concrete"), ("Réhabilitation lourde", "Heavy rehabilitation"), ("Reconstruction", "Reconstruction"), ("Tous corps d'état", "All trades"), ("Mise en conformité", "Compliance upgrades")],
  "Pompe à béton XCMG XS5008D, chariots télescopiques 14 m, outillage électroportatif complet.", "XCMG XS5008D concrete pump, 14 m telehandlers, full power tool set.",
  "Crèche et CLASS de Vieux-Habitants.", "Nursery and CLASS building in Vieux-Habitants."),
]

def page_expertises():
    h = head('expertises.html', "Nos expertises | TMI Travaux Modernes Ingénierie",
             "Réseaux humides, routes et enrobés, VRD et terrassement, travaux spéciaux et parasismique, bâtiment et génie civil : les cinq métiers de TMI.",
             title_en='Our expertise | TMI Travaux Modernes Ingénierie', desc_en="Water networks, roads and asphalt, utilities and earthworks, special foundations and seismic strengthening, building and civil engineering: TMI's five trades.")
    body = phero("Cinq expertises au service des territoires", "Five areas of expertise serving our islands",
                 "Nous réalisons nos chantiers avec nos propres équipes et notre propre parc, de l'étude d'exécution à la livraison.",
                 "We carry out our projects with our own teams and fleet, from detailed design to handover.",
                 'ref-gosier-fondations', "Expertises", "Expertise")
    body += '<nav class="exp-nav" aria-label="Expertises"><div class="wrap"><ul>' + ''.join(
        f'<li><a href="#{eid}" data-en="{a(en)}">{esc(fr)}</a></li>' for eid, _, fr, en, *_ in EXPERTISES) + '</ul></div></nav>'
    for eid, img, fr, en, dfr, den, subs, mfr, men, rfr, ren in EXPERTISES:
        subl = ''.join(f'<li data-en="{a(se)}">{esc(sf)}</li>' for sf, se in subs)
        body += f'''<section class="expertise" id="{eid}"><div class="wrap split">
  <div class="exp-photo">{pic(img, fr, en, sizes='(max-width:900px) 100vw, 560px')}</div>
  <div>
    <h2><a href="{SLUGS[eid]}" data-en="{a(en)}">{esc(fr)}</a></h2>
    {T(dfr, den, 'p', 'lead', style='margin-top:1.2rem')}
    <ul class="sublist">{subl}</ul>
    <div class="exp-refs"><strong data-en="Dedicated equipment">Matériel dédié</strong>{T(mfr, men)}</div>
    <div class="exp-refs"><strong data-en="Recent projects">Références récentes</strong>{T(rfr, ren)} <a class="link" href="{SLUGS[eid]}#references" data-en="See this trade's projects">Voir les réalisations du métier</a></div>
    <p style="margin-top:2rem"><a class="btn" href="{SLUGS[eid]}" data-en="Explore this trade">Découvrir le métier</a></p>
  </div>
</div></section>
'''
    body += f'''<section class="sect"><div class="wrap cta-row">
  {T("Parlons de votre opération", "Let's discuss your project", 'h2')}
  <div class="actions"><a class="btn" href="contact.html" data-en="Contact us">Nous consulter</a></div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Réalisations
def page_realisations():
    h = head('realisations.html', "Réalisations | TMI Travaux Modernes Ingénierie",
             "Les chantiers réalisés par TMI en 2025 : AEP à Petit-Canal, parasismique à Bergevin, enrobés à Saint-Martin, confortements, bâtiments publics.",
             title_en='Projects | TMI Travaux Modernes Ingénierie', desc_en='Projects delivered by TMI in 2025: water networks in Petit-Canal, seismic strengthening in Bergevin, asphalt in Saint-Martin, slope stabilisation, public buildings.')
    body = phero("Nos réalisations", "Our projects",
                 "Les chantiers en cours en 2026 et les opérations livrées en 2025 pour des maîtres d'ouvrage publics et privés, en Guadeloupe et à Saint-Martin.",
                 "Projects under way in 2026 and those delivered in 2025 for public and private clients in Guadeloupe and Saint-Martin.",
                 'ref-friars-bay', "Réalisations", "Projects")
    filt = '<button type="button" data-cat="all" aria-pressed="true" data-en="All">Toutes</button>' + ''.join(
        f'<button type="button" data-cat="{k}" aria-pressed="false" data-en="{a(v[1])}">{esc(v[0])}</button>' for k, v in CATS.items())
    cards = ''.join(card(r, link=CH_SLUG[r[0]]) for r in REFS)
    n_ec = sum(1 for c in CURRENT if c[1] is ST_EC)
    feat = ''.join(ccard(c) for c in CURRENT if c[6])
    rows = ''.join(crow(c) for c in CURRENT if not c[6])
    body += f'''<section class="sect" id="2026"><div class="wrap">
  <div class="sect-head">
    <div>{T("Actualité des chantiers", "Current projects", 'p', 'kicker')}{T("En 2026 : %d chantiers en cours" % n_ec, "In 2026: %d projects under way" % n_ec, 'h2')}</div>
    {T("Ouvrages portuaires, réseaux d'eau, aménagements, logements sociaux et équipements publics, pour des maîtres d'ouvrage publics de Guadeloupe et de Saint-Martin.", "Port works, water networks, developments, social housing and public facilities, for public clients in Guadeloupe and Saint-Martin.", 'p', 'lead')}
  </div>
  <div class="cards">{feat}</div>
  <ul class="crows">
    <li class="crow head" aria-hidden="true"><span data-en="Trade">Métier</span><span data-en="Project">Opération</span><span data-en="Client">Maître d'ouvrage</span><span data-en="Area">Territoire</span><span data-en="Amount">Montant</span><span data-en="Status">Statut</span></li>
    {rows}
  </ul>
  {T("TMI est également titulaire de plusieurs accords-cadres de voirie, d'enrobés, de réseaux d'eau et d'entretien de bâtiments auprès de collectivités de Guadeloupe et de Saint-Martin.", "TMI also holds several framework contracts for roads, asphalt, water networks and building maintenance with local authorities in Guadeloupe and Saint-Martin.", 'p', 'note', style='margin-top:2rem;font-size:1rem')}
</div></section>

<section class="sect tint" id="2025"><div class="wrap">
  <div class="sect-head">
    <div>{T("Références", "References", 'p', 'kicker')}{T("Chantiers livrés en 2025", "Projects delivered in 2025", 'h2')}</div>
    {T("Cliquez sur un chantier pour ouvrir sa fiche.", "Click a project to open its page.", 'p', 'lead')}
  </div>
  <div class="filters" role="group" aria-label="Filtrer par métier" data-en-label="Filter by trade">{filt}</div>
  <div class="summary" aria-live="polite"><span id="refs-count">15 chantiers présentés</span><span>{T("Montant cumulé", "Total value")} <strong id="refs-sum">{fmt_eur(sum(r[7] for r in REFS))}</strong></span></div>
  <div class="cards" id="refs-grid">{cards}</div>
</div></section>

'''
    return h + body + FOOT

# ---------------------------------------------------------------- Matériel
FLEET = [
 ("Terrassement et VRD", "Earthworks and utilities", [
   ("Mini-pelle 2,5 t", "Mini excavator 2.5 t", "8"), ("Pelle 6 t", "Excavator 6 t", "4"), ("Pelle 9 t", "Excavator 9 t", "1"), ("Pelle 15 t", "Excavator 15 t", "1"),
   ("Pelle sur pneus 16 t", "Wheeled excavator 16 t", "2"), ("Tractopelle", "Backhoe loader", "2")]),
 ("Transport", "Transport", [
   ("Camion benne", "Dump truck", "7"), ("Camion benne grue", "Dump truck with crane", "2"), ("Camion PL ampliroll grue 4×2", "Hook-lift crane truck 4×2", "1"),
   ("Camion grue ampliroll 6×4, 26 t", "Hook-lift crane truck 6×4, 26 t", "1"), ("Fourgon 11 m³", "Van 11 m³", "1")]),
 ("Routes et enrobés", "Roads and asphalt", [
   ("Raboteuse XCMG XM1505F|largeur 1,50 m", "Milling machine XCMG XM1505F|1.50 m width", "1"), ("Raboteuse XCMG XM1005F|largeur 1,00 m", "Milling machine XCMG XM1005F|1.00 m width", "1"),
   ("Finisseur XCMG RP705|table 2,55 à 7,50 m", "Paver XCMG RP705|2.55 to 7.50 m screed", "1"), ("Finisseur XCMG RP355|table 0,50 à 3,20 m", "Paver XCMG RP355|0.50 to 3.20 m screed", "1"),
   ("Compacteur tandem XCMG XD120S", "Tandem roller XCMG XD120S", "4"), ("Compacteur HAMM 12 t", "HAMM roller 12 t", "1"),
   ("Mini-chargeuse avec balayeuse et rabot 0,60 m", "Skid steer with sweeper and 0.60 m planer", "1"), ("Bouille à émulsion 2 000 L", "Emulsion sprayer 2,000 L", "1")]),
 ("Fondations spéciales : forage", "Special foundations: drilling", [
   ("Foreuse Comacchio MC8 HT", "Drilling rig Comacchio MC8 HT", "1"), ("Foreuse XCMG XLS4 200B", "Drilling rig XCMG XLS4 200B", "1"), ("Glissière Marini MR2-PN", "Marini MR2-PN slide", "2"),
   ("Ensemble de forage rotatif et percussion Marini EP120", "Marini EP120 rotary-percussion drilling unit", "2"), ("Marteau Montabert P21", "Montabert P21 hammer", "2")]),
 ("Fondations spéciales : air, injection, projection", "Special foundations: air, grouting, spraying", [
   ("Compresseurs Kaeser et Atlas Copco|5 à 24 m³", "Kaeser and Atlas Copco compressors|5 to 24 m³", "4"), ("Pompe à béton XCMG XS5008D|50 m³/h", "Concrete pump XCMG XS5008D|50 m³/h", "1"),
   ("Pompes à boue et à membrane", "Slurry and diaphragm pumps", "5"), ("Centrale d'injection automatisée", "Automated grouting plant", "1"), ("Malaxeurs et Mini Air Grout", "Mixers and Mini Air Grout", "3"),
   ("Unité de gunitage Arnabat MG305", "Arnabat MG305 shotcrete unit", "2")]),
 ("Manutention", "Handling", [
   ("Chariot télescopique Manitou MT1440|14 m", "Manitou MT1440 telehandler|14 m", "1"), ("Chariot télescopique XCMG XT4014KH|14 m", "XCMG XT4014KH telehandler|14 m", "1"),
   ("Chariot élévateur Heli 4 t", "Heli forklift 4 t", "1")]),
 ("Compactage et énergie", "Compaction and power", [
   ("Plaques vibrantes 45 à 400 kg", "Vibrating plates 45 to 400 kg", "8"), ("Rouleaux vibrants 800 kg", "Vibrating rollers 800 kg", "4"), ("Pieds de mouton télécommandés 1,5 t", "Remote-controlled sheepsfoot rollers 1.5 t", "4"),
   ("Groupes électrogènes 6 et 55 kVA", "Generators 6 and 55 kVA", "10"), ("Scies à sol", "Floor saws", "4"), ("Carotteuses Hilti DD 250", "Hilti DD 250 core drills", "2")]),
 ("Réseaux : contrôle et implantation", "Networks: control and setting out", [
   ("Lasers de canalisation", "Pipe lasers", "4"), ("Niveaux optiques sur trépied", "Optical levels on tripod", "4"), ("Niveaux laser", "Laser levels", "4"),
   ("Détecteurs de réseaux", "Utility detectors", "4"), ("Pompes d'exhaure", "Dewatering pumps", "4")]),
 ("Sécurité et signalisation", "Safety and signage", [
   ("Kits de signalisation temporaire", "Temporary signage kits", "60"), ("Feux tricolores de chantier", "Temporary traffic lights", "8"), ("Barrières", "Barriers", "20"),
   ("Projecteurs", "Floodlights", "6"), ("EPI complets pour chaque compagnon", "Full PPE for every worker", "")]),
]

def page_materiel():
    h = head('materiel.html', "Parc matériel | TMI Travaux Modernes Ingénierie",
             "Plus de 50 engins et véhicules en propre : raboteuses et finisseurs XCMG, foreuses Comacchio et XCMG, pelles, camions, compresseurs, matériel d'injection.",
             title_en='Equipment fleet | TMI Travaux Modernes Ingénierie', desc_en='More than 50 machines and vehicles of our own: XCMG milling machines and pavers, Comacchio and XCMG drilling rigs, excavators, trucks, compressors, grouting equipment.')
    body = phero("Un parc matériel en propre", "Our own equipment fleet",
                 "Plus de 50 engins et véhicules, entretenus par nos équipes et disponibles pour nos chantiers sans dépendre de la location.",
                 "More than 50 machines and vehicles, maintained by our teams and available for our sites without relying on rental.",
                 'materiel-finisseur', "Matériel", "Equipment")
    mos = ''.join(pic(n, af, ae) for n, af, ae in [
        ('materiel-finisseur', 'Finisseur XCMG RP355 sur le dépôt TMI', 'XCMG RP355 paver at the TMI yard'),
        ('materiel-foreuse', 'Foreuse de fondations spéciales', 'Special foundations drilling rig'),
        ('materiel-nuit', "Mise en œuvre d'enrobés de nuit", 'Night-time paving'),
        ('materiel-pelle-roues', 'Pelle sur pneus XCMG', 'XCMG wheeled excavator'),
        ('materiel-raboteuse', 'Raboteuse XCMG en cours de rabotage', 'XCMG milling machine at work')])
    groups = ''
    for gfr, gen, items in FLEET:
        rows = ''
        for fr, en, q in items:
            f1, _, f2 = fr.partition('|'); e1, _, e2 = en.partition('|')
            sub = f'<small data-en="{a(e2)}">{esc(f2)}</small>' if f2 else ''
            rows += f'<tr><td><span data-en="{a(e1)}">{esc(f1)}</span>{sub}</td><td>{q}</td></tr>'
        groups += f'<div>{T(gfr, gen, "h3")}<table>{rows}</table></div>'
    flag = [
     ('materiel-finisseur', "Mise en œuvre des enrobés", "Asphalt paving",
      [("2 finisseurs XCMG RP705 et RP355", "2 XCMG pavers, RP705 and RP355"), ("Largeur de table de 0,50 à 7,50 m", "Screed width from 0.50 to 7.50 m"), ("5 compacteurs tandem et cylindre 12 t", "5 tandem and 12 t rollers"), ("Bouille à émulsion 2 000 L", "2,000 L emulsion sprayer")]),
     ('materiel-raboteuse', "Rabotage", "Milling",
      [("2 raboteuses XCMG XM1505F et XM1005F", "2 XCMG milling machines, XM1505F and XM1005F"), ("Largeur de fraisage 1,00 m et 1,50 m", "1.00 m and 1.50 m milling width"), ("Mini-chargeuse avec rabot 0,60 m pour les reprises", "Skid steer with 0.60 m planer for patching"), ("Interventions de nuit", "Night work")]),
     ('materiel-foreuse', "Fondations spéciales", "Special foundations",
      [("Foreuses Comacchio MC8 HT et XCMG XLS4 200B", "Comacchio MC8 HT and XCMG XLS4 200B rigs"), ("2 ensembles de forage Marini EP120", "2 Marini EP120 drilling units"), ("Centrale d'injection automatisée", "Automated grouting plant"), ("2 unités de gunitage, compresseurs jusqu'à 24 m³", "2 shotcrete units, compressors up to 24 m³")]),
    ]
    fcards = ''
    for img, fr, en, items in flag:
        lis = ''.join(f'<li data-en="{a(e)}">{esc(f)}</li>' for f, e in items)
        fcards += f'<article class="flag"><div class="ph">{pic(img, fr, en)}</div><div class="bd">{T(fr, en, "h3")}<ul>{lis}</ul></div></article>'
    body += f'''<section class="sect"><div class="wrap">
  <div class="mosaic">{mos}</div>
  <dl class="figures" style="margin-top:clamp(48px,6vw,72px)">
    <div><dd>50+</dd>{T("engins et véhicules en propre", "machines and vehicles owned", 'dt')}</div>
    <div><dd>7,50 m</dd>{T("de largeur maximale de mise en œuvre des enrobés", "maximum paving width", 'dt')}</div>
    <div><dd>2</dd>{T("foreuses de fondations spéciales et leurs ateliers d'injection", "special foundation rigs with grouting plant", 'dt')}</div>
    <div><dd>2</dd>{T("territoires desservis : Guadeloupe et Saint-Martin", "territories served: Guadeloupe and Saint-Martin", 'dt')}</div>
  </dl>
</div></section>

<section class="sect dark on-dark"><div class="wrap">
  <div class="sect-head">
    <div>{T("Engins phares", "Key equipment", 'p', 'kicker')}{T("Des ateliers complets, prêts à mobiliser", "Complete crews' kit, ready to mobilise", 'h2')}</div>
    {T("Pour chaque métier, nous disposons de l'ensemble du matériel nécessaire, sans dépendre de la location pour démarrer un chantier.", "For each trade we own the full set of equipment needed, so we never depend on rental to start a project.", 'p', 'lead')}
  </div>
  <div class="flags">{fcards}</div>
</div></section>

<section class="sect"><div class="wrap">
  <div class="sect-head">
    <div>{T("Organisation du parc", "Fleet organisation", 'p', 'kicker')}{T("Un parc suivi, entretenu et disponible", "A fleet that is tracked, maintained and available", 'h2')}</div>
  </div>
  <div class="pillars">
    <div class="pillar">{T("Dépôts à Petit-Bourg", "Yards in Petit-Bourg", 'h3')}{T("Deux dépôts à Colin, au cœur de la Guadeloupe, pour stocker le matériel et préparer les chantiers.", "Two yards in Colin, in central Guadeloupe, to store equipment and prepare sites.", 'p')}</div>
    <div class="pillar">{T("Entretien en interne", "In-house maintenance", 'h3')}{T("Nos équipes assurent l'entretien courant et le suivi des engins pour limiter les immobilisations.", "Our teams handle routine maintenance and equipment follow-up to limit downtime.", 'p')}</div>
    <div class="pillar">{T("Partenaire XCMG", "XCMG partner", 'h3')}{T("Un parc largement équipé XCMG, avec un accès direct au constructeur et aux pièces aux Antilles.", "A fleet largely made up of XCMG machines, with direct access to the manufacturer and spare parts in the Caribbean.", 'p')}</div>
    <div class="pillar">{T("Mobilisation inter-îles", "Inter-island mobilisation", 'h3')}{T("Le matériel est déployé en Guadeloupe comme à Saint-Martin, où nous réalisons nos chantiers d'enrobés.", "Equipment is deployed in Guadeloupe and in Saint-Martin, where we carry out our paving projects.", 'p')}</div>
  </div>
</div></section>
<section class="sect tint" style="padding-top:clamp(56px,6vw,88px)"><div class="wrap">
  <div class="sect-head">
    <div>{T("Inventaire", "Inventory", 'p', 'kicker')}{T("Le matériel par métier", "Equipment by trade", 'h2')}</div>
    {T("Notre parc nous permet de tenir nos propres plannings, de mobiliser rapidement en cas d'urgence et de mener plusieurs chantiers en parallèle.", "Our fleet lets us set our own schedules, mobilise quickly in emergencies and run several sites in parallel.", 'p', 'lead')}
  </div>
  <div class="fleet">{groups}</div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Engagements
def page_engagements():
    h = head('engagements.html', "Nos engagements | TMI Travaux Modernes Ingénierie",
             "Sécurité, qualité, environnement et développement des compétences locales : les engagements de TMI sur ses chantiers.",
             title_en='Our commitments | TMI Travaux Modernes Ingénierie', desc_en="Safety, quality, environment and local skills development: TMI's commitments on every site.")
    body = phero("Nos engagements", "Our commitments",
                 "La sécurité, la propreté, la qualité, la gestion de l'environnement et le respect des délais sont nos priorités sur chacun de nos chantiers.",
                 "Safety, cleanliness, quality, environmental management and meeting deadlines are our priorities on every site.",
                 'ref-capesterre', "Engagements", "Commitments")
    blocks = [
     ('securite', 'pelle-brise-roche-nb', 500, 937, "Sécurité", "Safety",
      "La sécurité des compagnons, des usagers et des riverains passe avant tout. Nos équipes sont formées et équipées pour intervenir sur la voie publique, à proximité des réseaux et en hauteur.",
      "The safety of our workers, road users and residents comes first. Our teams are trained and equipped to work on public roads, near utilities and at height.",
      [("Sauveteurs secouristes du travail, formation renouvelée tous les deux ans", "First-aid at work, refreshed every two years"),
       ("AIPR : autorisation d'intervention à proximité des réseaux", "AIPR utility proximity certification"),
       ("Travaux en hauteur et port du harnais", "Work at height and harness use"),
       ("60 kits de signalisation temporaire, 8 feux de chantier", "60 temporary signage kits, 8 site traffic lights"),
       ("EPI complets, extincteurs et trousses de secours sur chantier", "Full PPE, extinguishers and first-aid kits on site")]),
     ('qualite', 'ref-rue-de-hollande', 1191, 653, "Qualité et délais", "Quality and deadlines",
      "Chaque opération est confiée à un conducteur de travaux et à un chef de chantier spécialistes du métier concerné. Notre matériel en propre nous permet de tenir les plannings, y compris en intervention d'urgence.",
      "Each project is assigned to a site manager and a foreman who specialise in the trade concerned. Owning our equipment lets us keep to schedule, including for emergency works.",
      [("Encadrement spécialisé par métier", "Trade-specialised supervision"),
       ("Implantation et contrôle : lasers, niveaux optiques", "Setting out and control: lasers, optical levels"),
       ("Essais et mise en service des réseaux", "Network testing and commissioning"),
       ("Dématérialisation : factures sur Chorus Pro, réponses électroniques aux appels d'offres", "Paperless: invoices via Chorus Pro, electronic tender submissions")]),
     ('environnement', 'ref-soufriere-urgence', 1191, 653, "Environnement", "Environment",
      "Nous travaillons dans des îles où l'eau, les sols et les paysages sont précieux. Nos chantiers intègrent la gestion du ruissellement, la protection des cours d'eau et la prévention des dommages aux réseaux existants.",
      "We work on islands where water, soil and landscapes are precious. Our sites include runoff management, stream protection and prevention of damage to existing networks.",
      [("Gestion des eaux pluviales et du ruissellement", "Stormwater and runoff management"),
       ("Curage et protection des cours d'eau", "Stream clearing and protection"),
       ("Détection des réseaux avant travaux", "Utility detection before works"),
       ("Chantiers propres et remise en état", "Clean sites and reinstatement")]),
     ('territoire', 'ouvrier-enrobe-nb', 543, 789, "Compétences et territoire", "Skills and local roots",
      "Notre vision : faire de TMI une plateforme qui investit dans les compétences locales. Nous formons nos collaborateurs tout au long de leur parcours et contribuons à l'insertion sociale dans nos îles.",
      "Our vision: make TMI a platform that invests in local skills. We train our people throughout their careers and contribute to social inclusion on our islands.",
      [("Plans de formation administratif, technique, sécurité et environnement", "Administrative, technical, safety and environmental training plans"),
       ("Formations qualifiantes, dont l'adduction d'eau potable avec l'Afpa", "Qualifying courses, including drinking water networks with Afpa"),
       ("Recrutement local en Guadeloupe et à Saint-Martin", "Local hiring in Guadeloupe and Saint-Martin")]),
    ]
    for i, (bid, img, w, hgt, fr, en, dfr, den, items) in enumerate(blocks):
        lis = ''.join(f'<li data-en="{a(e)}">{esc(f)}</li>' for f, e in items)
        tint = ' tint' if i % 2 else ''
        body += f'''<section class="sect{tint}" id="{bid}"><div class="wrap split">
  <div class="exp-photo">{pic(img, fr, en, sizes='(max-width:900px) 100vw, 560px')}</div>
  <div>{T(fr, en, 'h2')}{T(dfr, den, 'p', 'lead', style='margin-top:1.2rem')}<ul class="sublist" style="grid-template-columns:1fr">{lis}</ul></div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Carrières
def page_carrieres():
    h = head('carrieres.html', "Carrières | TMI Travaux Modernes Ingénierie",
             "Rejoignez TMI : conducteurs de travaux, chefs de chantier, conducteurs d'engins, canalisateurs, compagnons. Candidature en ligne.",
             title_en='Careers | TMI Travaux Modernes Ingénierie', desc_en='Join TMI: site managers, foremen, machine operators, pipelayers, skilled workers. Apply online.')
    body = phero("Rejoignez une entreprise qui grandit", "Join a growing company",
                 "Nos chantiers se multiplient en Guadeloupe et à Saint-Martin. Nous cherchons des femmes et des hommes de terrain qui partagent nos valeurs : engagement, rigueur, excellence.",
                 "Our project pipeline is growing in Guadeloupe and Saint-Martin. We are looking for hands-on people who share our values: commitment, rigour, excellence.",
                 'ref-petit-canal-aep', "Carrières", "Careers")
    jobs = [("Conducteur ou conductrice de travaux", "Site manager", "VRD, réseaux, enrobés, travaux spéciaux, génie civil.", "Utilities, networks, asphalt, special works, civil engineering."),
            ("Chef de chantier, chef d'équipe", "Site foreman, team leader", "Encadrement des équipes et organisation quotidienne du chantier.", "Leading crews and running the site day to day."),
            ("Conducteur d'engins", "Machine operator", "Pelles, raboteuses, finisseurs, compacteurs, foreuses.", "Excavators, milling machines, pavers, rollers, drilling rigs."),
            ("Canalisateur", "Pipe layer", "Pose de réseaux d'eau potable, d'eaux usées et pluviales.", "Laying drinking water, wastewater and stormwater pipes."),
            ("Compagnon VRD et enrobés", "Roads and asphalt worker", "Mise en œuvre des enrobés, bordures, trottoirs, réseaux.", "Paving, kerbs, pavements and utilities."),
            ("Coffreur-bancheur, maçon", "Formwork carpenter, mason", "Gros œuvre et béton armé, bâtiment et génie civil.", "Structural work and reinforced concrete.")]
    jl = ''.join(f'<div class="pillar">{T(f, e, "h3")}{T(df, de, "p")}</div>' for f, e, df, de in jobs)
    opts = ''.join(f'<option data-en="{a(e)}">{esc(f)}</option>' for f, e, *_ in jobs)
    body += f'''<section class="sect"><div class="wrap">
  <div class="sect-head">
    <div>{T("Nos métiers", "Our jobs", 'p', 'kicker')}{T("Les métiers de nos chantiers", "The jobs on our sites", 'h2')}</div>
    {T("Nous étudions toutes les candidatures, avec ou sans poste ouvert. Indiquez le métier visé et votre secteur.", "We consider every application, whether or not a position is open. Tell us the job you are looking for and your area.", 'p', 'lead')}
  </div>
  <div class="pillars p3">{jl}</div>
</div></section>

<section class="sect tint"><div class="wrap split top">
  <div>
    {T("Pourquoi TMI", "Why TMI", 'p', 'kicker')}
    {T("Grandir avec nous", "Grow with us", 'h2')}
    <ul class="sublist" style="grid-template-columns:1fr">
      <li data-en="Varied projects across five trades">Des chantiers variés sur cinq métiers</li>
      <li data-en="Modern equipment, mostly less than three years old">Un matériel moderne et entretenu</li>
      <li data-en="Training throughout your career: safety, AIPR, trade skills">Des formations tout au long du parcours : sécurité, AIPR, métiers</li>
      <li data-en="A human-sized company with ambition">Une entreprise à taille humaine, avec de l'ambition</li>
    </ul>
  </div>
  <div>
    {T("Candidature", "Application", 'h3', style='margin-bottom:1.2rem')}
    <form name="candidature" method="POST" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data">
      <input type="hidden" name="form-name" value="candidature">
      <p class="hp"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="row">
        <div class="field"><label for="c-nom" data-en="Full name">Nom et prénom</label><input id="c-nom" name="nom" autocomplete="name" required></div>
        <div class="field"><label for="c-tel" data-en="Phone">Téléphone</label><input id="c-tel" type="tel" name="telephone" autocomplete="tel" required></div>
      </div>
      <div class="row">
        <div class="field"><label for="c-mail">Email</label><input id="c-mail" type="email" name="email" autocomplete="email" required></div>
        <div class="field"><label for="c-zone" data-en="Area">Secteur</label><select id="c-zone" name="secteur"><option>Guadeloupe</option><option>Saint-Martin</option><option data-en="Both">Les deux</option></select></div>
      </div>
      <div class="field"><label for="c-job" data-en="Job">Métier visé</label><select id="c-job" name="metier"><option value="" data-en="Choose…">Choisir…</option>{opts}<option data-en="Other">Autre</option></select></div>
      <div class="field"><label for="c-cv" data-en="CV (PDF, 8 MB max)">CV (PDF, 8 Mo maximum)</label><input id="c-cv" type="file" name="cv" accept=".pdf,.doc,.docx"></div>
      <div class="field"><label for="c-msg" data-en="Message">Message</label><textarea id="c-msg" name="message" data-en-ph="Experience, qualifications (CACES, AIPR…), availability" placeholder="Expérience, habilitations (CACES, AIPR…), disponibilité"></textarea></div>
      <label class="check"><input type="checkbox" name="consentement" required> {T("J'accepte que TMI conserve ma candidature pour la durée du recrutement et au plus deux ans.", "I agree that TMI may keep my application for the recruitment period and for up to two years.")}</label>
      <button class="btn" type="submit" data-en="Send my application">Envoyer ma candidature</button>
    </form>
    <div class="form-msg" hidden data-en="Application received. We will get back to you.">Candidature reçue. Nous revenons vers vous.</div>
    <div class="form-msg err" hidden data-en="The application could not be sent. Please try again or email contact@tmi-caraibes.com.">La candidature n'a pas pu être envoyée. Réessayez ou écrivez à contact@tmi-caraibes.com.</div>
  </div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Contact
def page_contact():
    h = head('contact.html', "Contact | TMI Travaux Modernes Ingénierie",
             "Contactez TMI pour vos projets de réseaux, voirie, enrobés, VRD, travaux spéciaux et génie civil en Guadeloupe et à Saint-Martin.",
             title_en='Contact | TMI Travaux Modernes Ingénierie', desc_en='Contact TMI for your water network, road, asphalt, utilities, special foundations and civil engineering projects in Guadeloupe and Saint-Martin.')
    body = phero("Parlons de votre projet", "Tell us about your project",
                 "Collectivités, maîtres d'œuvre, entreprises, particuliers : quelle que soit votre demande, décrivez-la ici, nous revenons vers vous.",
                 "Public bodies, engineers, businesses, individuals: whatever your request, describe it here and we will get back to you.",
                 'ref-vieux-habitants-pont', "Contact", "Contact")
    types = [("Réseaux humides", "Water networks"), ("Routes et enrobés", "Roads and asphalt"), ("VRD et terrassement", "Utilities and earthworks"),
             ("Travaux spéciaux et parasismique", "Special works and seismic"), ("Bâtiment et génie civil", "Building and civil engineering"),
             ("Intervention d'urgence", "Emergency works"), ("Demande de devis", "Quote request"), ("Fournisseur ou sous-traitant", "Supplier or subcontractor"), ("Partenariat", "Partnership")]
    opts = ''.join(f'<option data-en="{a(e)}">{esc(f)}</option>' for f, e in types)
    body += f'''<section class="sect"><div class="wrap split top">
  <div>
    {T("Coordonnées", "Details", 'p', 'kicker')}
    {T("TMI Travaux Modernes Ingénierie", "TMI Travaux Modernes Ingénierie", 'h2', style='font-size:clamp(1.7rem,2.6vw,2.3rem)')}
    <dl class="coords">
      <div><dt data-en="Head office">Siège</dt><dd>{ADDR_FR}</dd></div>
      <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt data-en="Management">Direction</dt><dd data-en="Johane Devouton, President">Johane Devouton, Présidente</dd></div>
      <div><dt data-en="Area">Zone d'intervention</dt><dd>Guadeloupe, Saint-Martin</dd></div>
    </dl>
    <p style="margin-top:2rem"><a class="link" href="https://www.google.com/maps/search/?api=1&query=Tambour+Monplaisir+97170+Petit-Bourg" target="_blank" rel="noopener" data-en="Open in Google Maps">Ouvrir dans Google Maps</a></p>
  </div>
  <div>
    <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="contact">
      <p class="hp"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="row">
        <div class="field"><label for="f-nom" data-en="Name">Nom</label><input id="f-nom" name="nom" autocomplete="name" required></div>
        <div class="field"><label for="f-org" data-en="Organisation">Organisme ou entreprise</label><input id="f-org" name="organisme" autocomplete="organization"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-mail">Email</label><input id="f-mail" type="email" name="email" autocomplete="email" required></div>
        <div class="field"><label for="f-tel" data-en="Phone">Téléphone</label><input id="f-tel" type="tel" name="telephone" autocomplete="tel"></div>
      </div>
      <div class="field"><label for="f-type" data-en="Subject">Objet</label><select id="f-type" name="objet"><option value="" data-en="Choose…">Choisir…</option>{opts}<option data-en="Other request">Autre demande</option></select></div>
      <div class="field"><label for="f-msg" data-en="Your project">Votre projet</label><textarea id="f-msg" name="message" required data-en-ph="Location, type of works, timeline, documents available…" placeholder="Lieu, nature des travaux, délai, pièces disponibles…"></textarea></div>
      <button class="btn" type="submit" data-en="Send the request">Envoyer la demande</button>
    </form>
    <div class="form-msg" hidden data-en="Request sent. We will get back to you shortly.">Demande envoyée. Nous revenons vers vous rapidement.</div>
    <div class="form-msg err" hidden data-en="The request could not be sent. Please try again or email contact@tmi-caraibes.com.">La demande n'a pas pu être envoyée. Réessayez ou écrivez à contact@tmi-caraibes.com.</div>
  </div>
</div></section>
'''
    return h + body + FOOT

# ---------------------------------------------------------------- Mentions légales
def page_mentions():
    h = head('mentions-legales.html', "Mentions légales | TMI Travaux Modernes Ingénierie", "Mentions légales du site tmi-caraibes.com.",
             title_en="Legal notice | TMI Travaux Modernes Ingénierie", desc_en="Legal notice for tmi-caraibes.com.")
    if LANG == 'en':
        return h + f'''<section class="sect"><div class="wrap legal-text">
  <p class="crumbs" style="color:var(--gris)"><a href="index.html">Home</a> / Legal notice</p>
  <h1 style="font-size:clamp(2.2rem,4vw,3.4rem);margin-bottom:1rem">Legal notice</h1>
  <p style="color:var(--gris)">This English version is provided for convenience. The French version is the authoritative one.</p>
  <h2>Publisher</h2>
  <p>TMI Travaux Modernes Ingénierie, a French single-shareholder simplified joint-stock company (SASU) with a share capital of €1,000.<br>
  Registered office: Route de l'Hôtel, Tambour Monplaisir, 97170 Petit-Bourg, Guadeloupe, France.<br>
  Pointe-à-Pitre Trade and Companies Register 948 626 445, head office SIRET 948 626 445 00035.<br>
  EU VAT number: FR33 948 626 445.<br>
  Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p>Publication director: Johane Devouton, President.</p>
  <h2>Hosting</h2>
  <p>Netlify, Inc., 101 2nd Street, San Francisco, CA 94105, United States.<br>Website: <a href="https://www.netlify.com" target="_blank" rel="noopener">www.netlify.com</a></p>
  <h2>Intellectual property</h2>
  <p>The texts, photographs, logos and graphic elements of this website are the property of TMI or used with permission. Any reproduction without prior written consent is prohibited.</p>
  <h2>Personal data</h2>
  <p>Information submitted through the contact and application forms is used by TMI only to answer your request or review your application. It is not passed on to third parties. Applications are kept for two years at most. You may request access to, correction or deletion of your data by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p>The data controller is TMI, represented by its President. Messages sent through the forms are received by our hosting provider, Netlify, Inc., which may process them in the United States on our behalf before forwarding them to TMI by email. If you believe your rights are not respected, you may lodge a complaint with the French data protection authority, the CNIL (<a href="https://www.cnil.fr" target="_blank" rel="noopener">www.cnil.fr</a>).</p>
  <h2>Cookies</h2>
  <p>This website uses no audience-measurement or advertising cookies and loads no third-party service when pages are displayed (fonts are hosted on the site itself).</p>
</div></section>
''' + FOOT
    body = f'''<section class="sect"><div class="wrap legal-text">
  <p class="crumbs" style="color:var(--gris)"><a href="index.html" data-en="Home">Accueil</a> / {T("Mentions légales", "Legal notice")}</p>
  {T("Mentions légales", "Legal notice", 'h1', style='font-size:clamp(2.2rem,4vw,3.4rem);margin-bottom:1rem')}
  <h2>Éditeur du site</h2>
  <p>TMI Travaux Modernes Ingénierie, société par actions simplifiée unipersonnelle (SASU) au capital de 1 000 €.<br>
  Siège social : Route de l'Hôtel, Tambour Monplaisir, 97170 Petit-Bourg, Guadeloupe.<br>
  RCS Pointe-à-Pitre 948 626 445, SIRET du siège 948 626 445 00035.<br>
  TVA intracommunautaire : FR33 948 626 445.<br>
  Email : <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p>Directrice de la publication : Johane Devouton, Présidente.</p>
  <h2>Hébergement</h2>
  <p>Netlify, Inc., 101 2nd Street, San Francisco, CA 94105, États-Unis.<br>Site : <a href="https://www.netlify.com" target="_blank" rel="noopener">www.netlify.com</a></p>
  <h2>Propriété intellectuelle</h2>
  <p>Les textes, photographies, logos et éléments graphiques de ce site sont la propriété de TMI ou utilisés avec autorisation. Toute reproduction sans accord écrit préalable est interdite.</p>
  <h2>Données personnelles</h2>
  <p>Les informations transmises par les formulaires de contact et de candidature sont utilisées uniquement par TMI pour répondre à votre demande ou étudier votre candidature. Elles ne sont pas cédées à des tiers. Les candidatures sont conservées au plus deux ans. Vous pouvez demander l'accès, la rectification ou la suppression de vos données en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p>Le responsable du traitement est TMI, représentée par sa Présidente. Les messages envoyés par les formulaires sont réceptionnés par notre hébergeur, Netlify, Inc., qui peut les traiter aux États-Unis pour notre compte avant leur transmission à TMI par email. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL (<a href="https://www.cnil.fr" target="_blank" rel="noopener">www.cnil.fr</a>).</p>
  <h2>Cookies</h2>
  <p>Ce site n'utilise pas de cookie de mesure d'audience ni de publicité, et ne fait appel à aucun service tiers au chargement des pages (les polices de caractères sont hébergées sur le site). </p>
</div></section>
'''
    return h + body + FOOT

PAGES_EXTRA = {}
exec(open(os.path.join(HERE, 'activites.py'), encoding='utf-8').read())

PAGES = {
    'index.html': page_index, 'entreprise.html': page_entreprise, 'expertises.html': page_expertises,
    'realisations.html': page_realisations, 'materiel.html': page_materiel, 'engagements.html': page_engagements,
    'carrieres.html': page_carrieres, 'contact.html': page_contact, 'mentions-legales.html': page_mentions,
}
PAGES.update(PAGES_EXTRA)

from bs4 import BeautifulSoup

def to_en(html):
    """Applique les traductions portées par les attributs data-en* (même logique que l'ancien script)."""
    soup = BeautifulSoup(html, 'lxml')
    for el in soup.select('[data-en]'):
        el.string = el['data-en']
    for el in soup.select('[data-en-html]'):
        el.clear(); el.append(BeautifulSoup(el['data-en-html'], 'html.parser'))
    for el in soup.select('[data-en-ph]'):
        el['placeholder'] = el['data-en-ph']
    for el in soup.select('[data-en-alt]'):
        el['alt'] = el['data-en-alt']
    for el in soup.select('[data-en-label]'):
        el['aria-label'] = el['data-en-label']
    return str(soup)

def strip_i18n(html):
    return re.sub(r' data-(?:en|fr)(?:-html|-ph|-alt|-label)?="[^"]*"', '', html)

def finalize(html, lang):
    """Réécrit les liens internes X.html → adresses propres de la langue."""
    def sub(m):
        page, frag = m.group(1), m.group(2) or ''
        return f'href="{path_for(page, lang)}{frag}"'
    html = re.sub(r'href="([a-z0-9\-]+\.html)(#[^"]*)?"', sub, html)
    return strip_i18n(html)

def flatten(html, lang):
    """Variante à plat pour l'aperçu (artefact) : /x/ → x.html, /en/x/ → en-x.html, chemins relatifs."""
    def sub(m):
        path, frag = m.group(1), m.group(2) or ''
        if path == '/': return f'href="index.html{frag}"'
        if path == '/en/': return f'href="en-index.html{frag}"'
        parts = path.strip('/').split('/')
        return f'href="{"en-" + parts[1] if parts[0] == "en" else parts[0]}.html{frag}"'
    html = re.sub(r'href="(/(?:en/)?(?:[a-z0-9\-]+/)?)(#[^"]*)?"', sub, html)
    html = html.replace('"/img/', '"img/').replace(', /img/', ', img/').replace('"/assets/', '"assets/')
    return html

import shutil
os.makedirs(DIST, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
for old in glob.glob(os.path.join(DIST, '*')):
    if os.path.isdir(old) and os.path.basename(old) not in ('img', 'assets'):
        shutil.rmtree(old)
    elif os.path.isfile(old):
        os.remove(old)
for old in glob.glob(os.path.join(OUT, '*.html')):
    os.remove(old)

SITEMAP = []
for name, fn in PAGES.items():
    for lang in ('fr', 'en'):
        LANG = lang
        html = fn()
        if lang == 'en':
            html = to_en(html)
        html = finalize(html, lang)
        rel = path_for(name, lang).lstrip('/')
        d = os.path.join(DIST, rel)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        flat = ('index.html' if name == 'index.html' else name) if lang == 'fr' else ('en-index.html' if name == 'index.html' else 'en-' + EN_SLUG[name] + '.html')
        with open(os.path.join(OUT, flat), 'w', encoding='utf-8') as f:
            f.write(flatten(html, lang))
    SITEMAP.append(name)
LANG = 'fr'

# ---- sitemap (FR + EN, avec liens hreflang), robots, 404, redirections, en-têtes ----
TODAY = '2026-11-17'
def smurl(n, lang):
    other = 'en' if lang == 'fr' else 'fr'
    return (f'  <url><loc>{url_for(n, lang)}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq>'
            f'<priority>{"1.0" if n == "index.html" else "0.7"}</priority>\n'
            f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url_for(n, lang)}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="{other}" href="{url_for(n, other)}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_for(n, "fr")}"/>\n  </url>\n')
urls = ''.join(smurl(n, l) for n in SITEMAP for l in ('fr', 'en'))
open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')

LANG = 'fr'
nf = head('404.html', "Page introuvable | TMI", "Page introuvable.") + f'''<section class="sect"><div class="wrap">
  <h1 style="font-size:clamp(2rem,4vw,3rem);margin-bottom:1rem">Cette page n'existe pas ou a été déplacée.</h1>
  <p class="lead" style="margin-bottom:2rem">This page does not exist or has moved.</p>
  <div class="actions"><a class="btn" href="index.html">Retour à l'accueil</a><a class="btn line" href="/en/">Home (English)</a></div>
</div></section>''' + FOOT
nf = finalize(nf, 'fr')
open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(nf)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(flatten(nf, 'fr'))

redirects = ['# Anciennes adresses (.html) vers les adresses propres', '/index.html / 301!']
redirects += [f'/{n} {path_for(n, "fr")} 301!' for n in SITEMAP if n != 'index.html']
redirects += ['', '# Pages inexistantes', '/* /404.html 404']
open(os.path.join(DIST, '_redirects'), 'w').write('\n'.join(redirects) + '\n')

headers = '''/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://i.ytimg.com; font-src 'self'; frame-src https://www.youtube-nocookie.com; form-action 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/img/*
  Cache-Control: public, max-age=2592000

/sitemap.xml
  Cache-Control: public, max-age=3600
'''
open(os.path.join(DIST, '_headers'), 'w').write(headers)

# ---- fichiers statiques : CSS/JS/polices, images responsives ----
os.makedirs(os.path.join(DIST, 'assets'), exist_ok=True)
for sub in (OUT, DIST):
    os.makedirs(os.path.join(sub, 'assets', 'fonts'), exist_ok=True)
    shutil.copy(SRC + '/assets/style.css', sub + '/assets/style.css')
    shutil.copy(SRC + '/assets/site.js', sub + '/assets/site.js')
    for f in glob.glob(SRC + '/assets/fonts/*'):
        shutil.copy(f, sub + '/assets/fonts/')
exec(open(os.path.join(HERE, 'images.py'), encoding='utf-8').read())
print('ok', len(PAGES), 'pages ×2 langues')
