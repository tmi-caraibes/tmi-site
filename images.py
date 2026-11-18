# Images responsives : génère name-{480,800,1200,source}.webp depuis src/img/*.jpg, plus l'image de partage og-tmi.jpg.
from PIL import Image, ImageOps
import os, glob, shutil

def _save_variant(im, w, dest):
    v = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    v.save(dest, 'WEBP', quality=80 if w <= 800 else 78, method=6)

def build_images(dests):
    for d in dests:
        os.makedirs(os.path.join(d, 'img'), exist_ok=True)
    made = 0
    for srcf in sorted(glob.glob(os.path.join(SRC, 'img', '*.jpg'))):
        name = os.path.basename(srcf)[:-4]
        im = None
        for w in img_variants(name):
            out = f'{name}-{w}.webp'
            for d in dests:
                dest = os.path.join(d, 'img', out)
                if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(srcf):
                    continue
                if im is None:
                    im = ImageOps.exif_transpose(Image.open(srcf)).convert('RGB')
                _save_variant(im, w, dest)
                made += 1
    # Image de partage (Open Graph) : 1200 × 630 en JPEG, format accepté par tous les réseaux
    hero = ImageOps.exif_transpose(Image.open(os.path.join(SRC, 'img', 'hero-voirie.jpg'))).convert('RGB')
    og = ImageOps.fit(hero, (1200, 630), Image.LANCZOS, centering=(0.5, 0.5))
    for d in dests:
        dest = os.path.join(d, 'img', 'og-tmi.jpg')
        if not os.path.exists(dest):
            og.save(dest, 'JPEG', quality=85, optimize=True, progressive=True)
    for f in glob.glob(os.path.join(SRC, 'img', '*.png')):
        for d in dests:
            shutil.copy(f, os.path.join(d, 'img', os.path.basename(f)))
    # Supprime les anciens fichiers non générés (jpg/webp sans suffixe de largeur)
    keep = set()
    for srcf in glob.glob(os.path.join(SRC, 'img', '*.jpg')):
        name = os.path.basename(srcf)[:-4]
        keep |= {f'{name}-{w}.webp' for w in img_variants(name)}
    keep |= {os.path.basename(f) for f in glob.glob(os.path.join(SRC, 'img', '*.png'))} | {'og-tmi.jpg'}
    for d in dests:
        for f in glob.glob(os.path.join(d, 'img', '*')):
            if os.path.basename(f) not in keep:
                os.remove(f)
    return made

print('images générées :', build_images([DIST, OUT]))
