"""Check static links, duplicate IDs, source counts, and local image availability."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.references = []
        self.projects = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'data-project' in attrs:
            self.projects += 1
        for key in ('src', 'href'):
            if key in attrs:
                self.references.append(attrs[key])
        if attrs.get('target') == '_blank':
            assert 'noopener' in attrs.get('rel', ''), attrs


document = Document()
document.feed((ROOT / 'index.html').read_text())
used_assets = set()
assert len(document.ids) == len(set(document.ids)), 'Duplicate IDs'
for reference in document.references:
    if reference.startswith('#'):
        assert reference[1:] in document.ids, f'Missing target: {reference}'
    elif not reference.startswith(('https:', 'mailto:', 'tel:')):
        assert (ROOT / reference).is_file(), f'Missing asset: {reference}'
        used_assets.add((ROOT / reference).resolve())

for stylesheet in list(used_assets):
    if stylesheet.suffix != '.css':
        continue
    for reference in re.findall(r'url\([\"\']?([^\)\"\']+)', stylesheet.read_text()):
        asset = (stylesheet.parent / reference).resolve()
        assert asset.is_file(), f'Missing CSS asset: {reference}'
        used_assets.add(asset)
unused = {path.resolve() for path in (ROOT / 'assets').rglob('*') if path.is_file()} - used_assets
assert not unused, f'Unused assets: {unused}'

data = json.loads((ROOT / 'data/portfolio.json').read_text())
assert document.projects == len(data['repos']), 'Missing or duplicate repository cards'
for repo in data['repos']:
    assert repo['url'] in document.references, f'Missing repository link: {repo["name"]}'
for experience in data['experiences']:
    assert experience['id'] in document.ids, f'Missing experience: {experience["id"]}'
assert 'href="#0"' not in (ROOT / 'index.html').read_text(), 'Placeholder link'
print(f'PASS: {len(document.references)} references, {len(document.ids)} IDs, no missing/unused assets, and {document.projects} repositories.')
