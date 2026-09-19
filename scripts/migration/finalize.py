import json, os, re
from html import escape as html_escape

SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRATCH, 'out')
PROJ = '/home/simonredfern/Documents/workspace_2024/3rdPartyInfluence'
CONTENT = os.path.join(PROJ, 'src', 'content')
os.makedirs(CONTENT, exist_ok=True)

photos = json.load(open(os.path.join(OUT, 'photos.json'), encoding='utf8'))
idmap = json.load(open(os.path.join(OUT, 'idmap.json'), encoding='utf8'))

NAV = [
    ('3pi-rootz-and-hiztory', '3PI Rootz and Hiztory', 'Rootz'),
    ('module-co2e', 'Module CO2e', 'CO2e'),
    ('modular-learning', 'Modular Learning Sessions', 'Learning'),
    ('modular-transport', 'Modular Transport', 'Transport'),
    ('sequencer-software', 'Sequencer Software', 'Sequencer'),
    ('media-assets', 'Media Assets', 'Media'),
    ('gig-archive', 'Gig Archive', 'Gigs'),
    ('artists-activists-and-audiences', 'Artists Activists and Audiences', 'AAA'),
    ('corporate-and-sporting-events', 'Corporate, Sporting and Education events', 'Corporate'),
    ('modular-artists-for-planet-and-peoples', 'Modular Artists For Planet and Peoples', 'MAPP'),
]

COMPONENTS = {
    'Photo': '$lib/components/Photo.svelte',
    'Embed': '$lib/components/Embed.svelte',
    'Columns': '$lib/components/Columns.svelte',
    'Column': '$lib/components/Column.svelte',
    'NextGig': '$lib/components/NextGig.svelte',
    'GigList': '$lib/components/GigList.svelte',
}

def fix_text(t):
    # Collapse adjacent strong runs: **a****b** -> **ab**
    prev = None
    while prev != t:
        prev = t
        t = t.replace('****', '')
    return t

md_files = []
for root, _dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith('.md'):
            md_files.append(os.path.relpath(os.path.join(root, f), OUT))

all_pages = []
for fn in sorted(md_files):
    slug = fn[:-3].replace(os.sep, '/')
    raw = open(os.path.join(OUT, fn), encoding='utf8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, flags=re.S)
    fm, body = m.group(1), m.group(2)

    # Rewrite photo ids to their downloaded slugs
    def repl(mm):
        old = mm.group(1)
        new = idmap.get(old)
        if new is None or new not in photos:
            raise SystemExit(f'unmapped photo id {old!r} in {fn}')
        return f'<Photo id="{new}" />'
    body = re.sub(r'<Photo id="([^"]+)" />', repl, body)
    body = fix_text(body)

    lines = body.split('\n')

    if slug == 'index':
        # "Next Gig:" and the gig heading under it are data, not prose - they come
        # from gigs.json via <NextGig /> so the homepage and the archive cannot drift.
        out, skipping = [], False
        for ln in lines:
            if ln.startswith('## Next Gig'):
                out.extend(['<NextGig />', ''])
                skipping = True
                continue
            if skipping:
                if not ln.strip():
                    continue
                skipping = False
                if ln.startswith('## '):
                    continue
            out.append(ln)
        # Trailing "## Links" block becomes the site nav
        if '## Links' in out:
            out = out[:out.index('## Links')]
        lines = out

    if slug == 'gig-archive':
        # Replace the hand-written gig list with the shared data source
        keep = []
        for ln in lines:
            if ln.strip() == 'Plus Many others':
                continue
            keep.append(ln)
        lines = ['<GigList />', '', 'Plus many others.']

    body = '\n'.join(lines).strip()
    body = re.sub(r'\n{3,}', '\n\n', body)

    used = [c for c in COMPONENTS if re.search(rf'<{c}[ />]', body)]
    script = ''
    if used:
        imports = '\n'.join(f"\timport {c} from '{COMPONENTS[c]}';" for c in sorted(used))
        script = f'<script>\n{imports}\n</script>\n\n'

    dest = os.path.join(CONTENT, fn)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf8').write(f'---\n{fm}\n---\n\n{script}{body}\n')

    meta = dict(re.findall(r'^(\w+): (.*)$', fm, flags=re.M))
    all_pages.append({
        'path': '' if slug == 'index' else slug,
        'title': json.loads(meta.get('title', '""')),
        'description': json.loads(meta.get('description', '""')),
    })
    print(f'{slug:48s} components: {",".join(sorted(used)) or "-"}')

def md_to_html(t):
    if not t:
        return ''
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: f'<a href="{html_escape(m.group(2))}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    return t.replace('&#123;', '{').replace('&#125;', '}').strip()

# Notion falls back to the literal word "image" when a block has no alt text. That is
# not a caption, and as alt text it is worse than nothing - screen readers already
# announce the role. Drop it rather than rendering a meaningless line under the photo.
PLACEHOLDER = {'image', 'images', 'photo', 'img', 'untitled', ''}

for rec in photos.values():
    if (rec.get('caption') or '').strip().lower() in PLACEHOLDER:
        rec['caption'] = ''
    rec['captionHtml'] = md_to_html(rec.get('caption'))
    rec['alt'] = re.sub(r'\s{2,}', ' ', re.sub(r'<[^>]+>', '', rec.get('alt') or '')).strip()
    if rec['alt'].strip().lower() in PLACEHOLDER:
        rec['alt'] = ''

json.dump(photos, open(os.path.join(PROJ, 'src', 'lib', 'data', 'photos.json'), 'w', encoding='utf8'),
          indent=2, ensure_ascii=False)

json.dump(sorted(all_pages, key=lambda p: p['path']),
          open(os.path.join(PROJ, 'src', 'lib', 'data', 'pages.json'), 'w', encoding='utf8'),
          indent=2, ensure_ascii=False)
json.dump([{'slug': s, 'title': t, 'short': sh} for s, t, sh in NAV],
          open(os.path.join(PROJ, 'src', 'lib', 'data', 'nav.json'), 'w', encoding='utf8'),
          indent=2, ensure_ascii=False)
print(f'\npages.json: {len(all_pages)}   nav.json: {len(NAV)}')
