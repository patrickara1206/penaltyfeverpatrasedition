"""Import reviewed logo sources, validating each image before updating the catalogue.

Usage: python tools/import-logo-sources.py reviewed-sources.json
The input maps teams/competitions to explicit name, url and source records.
Name matching and source review happen before this step; failures preserve assets.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64, datetime, hashlib, io, json, re, sys, urllib.request, zipfile, xml.etree.ElementTree as ET
from PIL import Image

app = Path(__file__).resolve().parents[1] / 'app'
plan = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
source_by_url = {row['url']: row for rows in plan.values() for row in rows.values()}
logos = json.loads((app / 'logos.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
manifest = json.loads((app / 'logos-manifest.json').read_text(encoding='utf-8'))
cache = app.parent.parent / 'logo-research-2026' / 'downloads'
cache.mkdir(parents=True, exist_ok=True)

def download(url):
    try:
        key = hashlib.sha256(url.encode()).hexdigest()
        cached = cache / key
        if cached.exists():
            body = cached.read_bytes()
        else:
            if '--cache-only' in sys.argv:
                raise ValueError('Source not cached; preserved existing artwork')
            request = urllib.request.Request(url, headers={'User-Agent': 'PF-Logo-Catalogue/1.0 (asset verification)'})
            with urllib.request.urlopen(request, timeout=25) as response:
                body = response.read(8 * 1024 * 1024 + 1)
            if len(body) > 8 * 1024 * 1024:
                raise ValueError('Image exceeds size limit')
            if url.startswith('https://apps.difutbol.org/proxy.php?'):
                response = json.loads(body)
                payload = response.get('data', response.get('result', response))
                body = base64.b64decode(payload['value'], validate=True)
            if source_by_url[url].get('archive_member'):
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    info = archive.getinfo(source_by_url[url]['archive_member'])
                    if info.file_size > 8 * 1024 * 1024:
                        raise ValueError('Archive image exceeds size limit')
                    body = archive.read(info)
        extension = '.png'
        if b'<svg' in body[:1000]:
            root = ET.fromstring(body)
            if not root.tag.endswith('svg'):
                raise ValueError('Invalid SVG root')
            for element in root.iter():
                if element.tag.split('}')[-1].lower() in {'script', 'foreignobject', 'image'}:
                    raise ValueError('SVG contains active or external content')
                if element.tag.split('}')[-1].lower() == 'style':
                    css = ''.join(element.itertext()).lower()
                    if '@import' in css or re.search(r'url\(\s*[\"\x27]?\s*(?!#)[a-z/:]', css):
                        raise ValueError('SVG stylesheet contains external references')
                for attribute, value in element.attrib.items():
                    if attribute.lower().startswith('on') or (attribute.split('}')[-1] == 'href' and not value.startswith('#')):
                        raise ValueError('SVG contains event handlers or external references')
            extension = '.svg'
        else:
            with Image.open(io.BytesIO(body)) as image:
                image.verify()
            with Image.open(io.BytesIO(body)) as image:
                if min(image.size) < 16:
                    raise ValueError('Image too small')
                if image.format != 'PNG' or max(image.size) > 384:
                    output = io.BytesIO()
                    if image.mode not in {'1', 'L', 'LA', 'P', 'RGB', 'RGBA', 'I', 'I;16'}:
                        image = image.convert('RGB')
                    image.thumbnail((384, 384), Image.Resampling.LANCZOS)
                    image.save(output, format='PNG', optimize=True)
                    body = output.getvalue()
            # Lossless WebP preserves crest pixels and transparency while reducing
            # the portable bundle; keep PNG when it compresses more efficiently.
            with Image.open(io.BytesIO(body)) as image:
                output = io.BytesIO()
                image.save(output, format='WEBP', lossless=True, method=6)
                if len(output.getvalue()) < len(body) * 0.9:
                    body = output.getvalue()
                    extension = '.webp'
                elif image.format == 'WEBP':
                    extension = '.webp'
        cached.write_bytes(body)
        relative = 'assets/logos/' + key[:16] + extension
        (app / relative).write_bytes(body)
        return url, {'path': relative, 'sha256': hashlib.sha256(body).hexdigest()}
    except Exception as error:
        return url, {'error': str(error)[:180]}

urls = sorted({row['url'] for rows in plan.values() for row in rows.values()})
with ThreadPoolExecutor(max_workers=4) as executor:
    jobs = [executor.submit(download, url) for url in urls]
    results = {}
    for job in as_completed(jobs):
        url, result = job.result()
        results[url] = result
        if len(results) % 50 == 0:
            print('Validated ' + str(len(results)) + '/' + str(len(urls)), flush=True)
report = {'checked_at': datetime.date.today().isoformat(), 'updated': {}, 'errors': []}
for kind, rows in plan.items():
    report['updated'][kind] = []
    for key, row in rows.items():
        result = results[row['url']]
        if 'error' in result:
            report['errors'].append({'kind': kind, 'name': key, 'url': row['url'], 'error': result['error']})
            continue
        record = {**row, **result, 'checked_at': report['checked_at']}
        logos[kind][key] = result['path']
        manifest[kind][key] = record
        report['updated'][kind].append(key)

(app / 'logos.js').write_text('window.PF_LOGOS=' + json.dumps(logos, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
(app / 'logos-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
data = json.loads((app / 'data.json').read_text(encoding='utf-8'))
current = {name for competition in data['competitions'] if not competition.get('historical') for name in competition['teams']}
report['unverified_monograms'] = sorted(name for name in current if '/edition/' in logos['teams'].get(name, ''))
report['unverified_competitions'] = sorted(competition['id'] for competition in data['competitions'] if '/edition/' in logos['competitions'].get(competition['id'], ''))
report['limitations'] = 'Source retrieval is not official certification of a 2026 redesign. Unverified identities retain clearly identifiable fallback artwork.'
(app / 'logo-audit-current.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'updated': {key: len(value) for key, value in report['updated'].items()}, 'teams_pending': len(report['unverified_monograms']), 'competitions_pending': len(report['unverified_competitions']), 'errors': len(report['errors'])}))
