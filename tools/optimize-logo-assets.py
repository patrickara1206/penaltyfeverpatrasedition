"""Convert remaining PNG catalogue assets to smaller, pixel-verified lossless WebP."""
from pathlib import Path
from PIL import Image, ImageChops
import hashlib, io, json

app = Path(__file__).resolve().parents[1] / 'app'
logos = json.loads((app / 'logos.js').read_text(encoding='utf8').split('=', 1)[1].strip().rstrip(';'))
manifest = json.loads((app / 'logos-manifest.json').read_text(encoding='utf8'))
replacements = {}
saved = 0
for relative in sorted({path for rows in logos.values() for path in rows.values()}):
    if not relative.endswith('.png'):
        continue
    raw = (app / relative).read_bytes()
    with Image.open(io.BytesIO(raw)) as source:
        original = source.convert('RGBA')
        output = io.BytesIO()
        original.save(output, format='WEBP', lossless=True, method=6)
    encoded = output.getvalue()
    if len(encoded) >= len(raw) * 0.9:
        continue
    with Image.open(io.BytesIO(encoded)) as decoded:
        restored = decoded.convert('RGBA')
        assert ImageChops.difference(original.getchannel('A'), restored.getchannel('A')).getbbox() is None
        for color in ['black', 'white']:
            background = Image.new('RGBA', original.size, color)
            before = Image.alpha_composite(background, original).convert('RGB')
            after = Image.alpha_composite(background, restored).convert('RGB')
            assert ImageChops.difference(before, after).getbbox() is None, relative
    replacement = 'assets/logos/' + hashlib.sha256(raw).hexdigest()[:16] + '.webp'
    (app / replacement).write_bytes(encoded)
    replacements[relative] = (replacement, hashlib.sha256(encoded).hexdigest())
    saved += len(raw) - len(encoded)

for kind, rows in logos.items():
    for name, relative in rows.items():
        if relative in replacements:
            replacement, digest = replacements[relative]
            rows[name] = replacement
            manifest[kind][name].update(path=replacement, sha256=digest, encoding='lossless WebP; decoded visible pixels and alpha verified')
(app / 'logos.js').write_text('window.PF_LOGOS=' + json.dumps(logos, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf8')
(app / 'logos-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'converted': len(replacements), 'bytes_saved': saved, 'visible_pixels_and_alpha': 'identical'}))
