# Site web TMI — tmi-caraibes.com

Site statique bilingue (FR / EN) généré par `build.py`, hébergé sur Netlify.

## Structure

- `build.py`, `activites.py`, `images.py` — générateur (contenu des pages, pages métier et fiches chantier, images responsives)
- `src/` — sources : feuille de style, script, polices, photos d'origine (`src/img/*.jpg`)
- `dist/` — site généré, publié par Netlify (adresses propres, `/en/` pour l'anglais, `_redirects`, `_headers`, `sitemap.xml`)

## Mettre à jour le site

1. Modifier le contenu dans `build.py` ou `activites.py` (ou ajouter une photo dans `src/img/`).
2. Lancer `python3 build.py` (Python 3 avec Pillow, beautifulsoup4 et lxml).
3. Vérifier en local : `python3 serve_dist.py` puis ouvrir http://127.0.0.1:8765/ (ou `python3 test_dist.py` pour le contrôle automatique).
4. Valider et pousser (`git commit`, `git push`) : Netlify déploie automatiquement.

## Vidéos de chantier (enrobés)

Dans `activites.py`, renseigner l'identifiant YouTube dans `VIDEOS`, par exemple
`'chantier-enrobe-friars-bay-saint-martin.html': 'identifiant'`, puis relancer `build.py`.
