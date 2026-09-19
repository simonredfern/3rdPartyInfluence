import re, json, glob, html, os
from html.parser import HTMLParser

SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRATCH, 'out')

PAGES = [
    ('page.html', '', 'Home'),
    ('p_3pi-rootz-and-hiztory.html', '3pi-rootz-and-hiztory', '3PI Rootz and Hiztory'),
    ('p_modular-learning.html', 'modular-learning', 'Modular Learning Sessions'),
    ('p_module-co2e.html', 'module-co2e', 'Module CO2e'),
    ('p_modular-transport.html', 'modular-transport', 'Modular Transport'),
    ('p_modular-artists-for-planet-and-peoples.html', 'modular-artists-for-planet-and-peoples', 'Modular Artists For Planet and Peoples'),
    ('p_artists-activists-and-audiences.html', 'artists-activists-and-audiences', 'Artists Activists and Audiences'),
    ('p_corporate-and-sporting-events.html', 'corporate-and-sporting-events', 'Corporate, Sporting and Education events'),
    ('p_sequencer-software.html', 'sequencer-software', 'Sequencer Software'),
    ('p_gig-archive.html', 'gig-archive', 'Gig Archive'),
    ('p_media-assets.html', 'media-assets', 'Media Assets'),
    ('p_aaa-upcoming.html', 'artists-activists-and-audiences/aaa-upcoming', 'AAA Upcoming'),
]

class Node:
    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.kids = []
        self.text = ''
    def cls(self):
        return self.attrs.get('class', '')

VOID = {'img','br','hr','input','meta','link','source','circle','rect','stop','path','use'}

class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].kids.append(Node(tag, attrs))
    def handle_endtag(self, tag):
        if tag in VOID: return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return
    def handle_data(self, data):
        n = Node('#text'); n.text = data
        self.stack[-1].kids.append(n)

def esc_md(s):
    # Escape only what would break markdown/mdsvex
    return s.replace('\\', '\\\\').replace('{', '&#123;').replace('}', '&#125;').replace('<', '&lt;').replace('>', '&gt;')

def emph(t, marker):
    """Wrap in emphasis markers while keeping surrounding whitespace outside them."""
    core = t.strip()
    if not core:
        return t
    lead = t[:len(t) - len(t.lstrip())]
    trail = t[len(t.rstrip()):]
    return f'{lead}{marker}{core}{marker}{trail}'

def inline(node):
    """Render inline content (text, links, strong, em) to markdown."""
    out = []
    for k in node.kids:
        if k.tag == '#text':
            out.append(esc_md(k.text))
        elif k.tag == 'a':
            href = k.attrs.get('href', '')
            label = inline(k).strip()
            if not label: continue
            out.append(f'[{label}]({href})')
        elif k.tag in ('strong', 'b'):
            out.append(emph(inline(k), '**'))
        elif k.tag in ('em', 'i'):
            out.append(emph(inline(k), '*'))
        elif k.tag in ('br',):
            out.append('\n')
        elif k.tag in ('svg', 'script', 'style'):
            continue
        else:
            out.append(inline(k))
    return ''.join(out)

def plain(node):
    out = []
    for k in node.kids:
        if k.tag == '#text': out.append(k.text)
        elif k.tag in ('svg','script','style'): continue
        else: out.append(plain(k))
    return ''.join(out)

IMG_BASE = re.compile(r'(https://images\.spr\.so/[^\s"\']+?)/(?:public|w=\d+[^\s"\']*)')

def img_key(url):
    m = IMG_BASE.match(url)
    base = m.group(1) if m else url
    return base.rsplit('/', 1)[-1], base

CREDIT_RX = re.compile(
    r'[\s.,\-–—]*\b(?:photo(?:graph(?:er|y)?)?|phtographer|pic|image|shot)\s*(?:by|:)?[\s:]*(\S.*)$',
    re.I | re.S)
HANDLE_RX = re.compile(r'@?\[([^\]]+)\]\(([^)]+)\)')

def split_credit(caption_md):
    """Split a trailing photographer credit off a markdown caption.
    Returns (caption, credit_name, credit_url)."""
    if not caption_md:
        return caption_md, None, None
    m = CREDIT_RX.search(caption_md)
    if not m:
        return caption_md.strip(), None, None
    credit_md = m.group(1).strip(' .,…')
    caption = caption_md[:m.start()].strip(' .,…\n')
    url = None
    hm = HANDLE_RX.search(credit_md)
    if hm:
        url = hm.group(2)
        credit_md = HANDLE_RX.sub(lambda x: '@' + x.group(1), credit_md)
    credit_md = re.sub(r'\s*@\s*', ' @', credit_md).strip(' .,@')
    credit_md = re.sub(r'\s{2,}', ' ', credit_md)
    # A "credit" longer than a name is really caption prose - reject it
    if not credit_md or len(credit_md.split()) > 6:
        return caption_md.strip(), None, None
    return caption, credit_md, url


images = {}

def register_image(url, alt, caption_md, caption_txt, w, h, page):
    name, base = img_key(url)
    source_md = caption_md or esc_md(alt or '')
    cap, credit, credit_url = split_credit(source_md)
    # Plain-text caption, for alt text
    cap_plain = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', cap)
    cap_plain = re.sub(r'[*_`]', '', cap_plain).strip()
    rec = images.setdefault(name, {
        'name': name, 'base': base, 'alt': '', 'caption': '',
        'credit': None, 'creditUrl': None, 'pages': []
    })
    if cap and not rec['caption']:
        rec['caption'] = cap
    if not rec['alt']:
        rec['alt'] = cap_plain or (alt or '').strip()
    if credit and not rec['credit']:
        rec['credit'] = credit
        rec['creditUrl'] = credit_url
    if page not in rec['pages']:
        rec['pages'].append(page)
    return name

def find_img(node):
    if node.tag == 'img': return node
    for k in node.kids:
        r = find_img(k)
        if r is not None: return r
    return None

def find_iframe(node):
    if node.tag == 'iframe': return node
    for k in node.kids:
        r = find_iframe(k)
        if r is not None: return r
    return None

def find_cls(node, cls):
    if cls in node.cls(): return node
    for k in node.kids:
        r = find_cls(k, cls)
        if r is not None: return r
    return None

def block(node, page, depth=0):
    """Render a block-level node to markdown lines."""
    c = node.cls()
    t = node.tag
    out = []

    if t in ('script', 'style', 'svg', 'nav'):
        return out

    if 'notion-image' in c:
        im = find_img(node)
        if im is None: return out
        src = im.attrs.get('src', '')
        fig = find_cls(node, 'notion-caption')
        cap_md = inline(fig).strip() if fig is not None else ''
        cap_txt = plain(fig).strip() if fig is not None else ''
        name = register_image(src, im.attrs.get('alt', ''), cap_md, cap_txt,
                              im.attrs.get('width'), im.attrs.get('height'), page)
        out.append(f'<Photo id="{name}" />')
        return out

    if 'notion-embed' in c:
        fr = find_iframe(node)
        if fr is None: return out
        src = html.unescape(fr.attrs.get('src', ''))
        src = re.split(r'["\'<]', src)[0]
        title = fr.attrs.get('title', '')
        out.append(f'<Embed src="{src}" title="{title}" />')
        return out

    if t in ('h1','h2','h3','h4','h5','h6') or 'notion-heading' in c:
        lvl = int(t[1]) if t.startswith('h') and t[1].isdigit() else 2
        txt = inline(node).strip()
        m2 = re.fullmatch(r'\*\*(.+)\*\*', txt, flags=re.S)
        if m2 and '**' not in m2.group(1):
            txt = m2.group(1).strip()
        if txt: out.append('#' * max(2, lvl) + ' ' + txt)
        return out

    if 'notion-column-list' in c:
        out.append('<Columns>')
        for k in node.kids:
            if 'notion-column' in k.cls():
                out.append('<Column>')
                for kk in k.kids:
                    out.extend(block(kk, page, depth + 1))
                out.append('</Column>')
        out.append('</Columns>')
        return out

    if t in ('ul', 'ol') or 'notion-bulleted-list' in c or 'notion-numbered-list' in c:
        marker = '1.' if t == 'ol' or 'numbered' in c else '-'
        for li in node.kids:
            if li.tag != 'li' and 'notion-list-item' not in li.cls():
                out.extend(block(li, page, depth))
                continue
            txt = inline(li).strip()
            if txt: out.append(f'{marker} {txt}')
        return out

    if t in ('p',) or 'notion-text' in c:
        # A notion-text div may wrap nested blocks; check for block children first
        has_block = any(
            ('notion-image' in k.cls() or 'notion-embed' in k.cls() or 'notion-column-list' in k.cls()
             or k.tag in ('ul','ol','h1','h2','h3'))
            for k in node.kids)
        if has_block:
            for k in node.kids:
                out.extend(block(k, page, depth))
            return out
        txt = inline(node).strip()
        if txt: out.append(txt)
        return out

    if t == 'a' and ('notion-page' in c or 'notion-link' in c):
        label = plain(node).strip()
        href = node.attrs.get('href', '')
        if label: out.append(f'- [{label}]({href})')
        return out

    # generic container: recurse
    for k in node.kids:
        if k.tag == '#text':
            if k.text.strip(): out.append(esc_md(k.text.strip()))
        else:
            out.extend(block(k, page, depth))
    return out

def extract(fname, slug, title):
    src = open(os.path.join(SCRATCH, fname), encoding='utf8', errors='ignore').read()
    m = re.search(r'<article[^>]*class="notion-root.*?</article>', src, flags=re.S)
    if not m:
        raise SystemExit(f'no article in {fname}')
    tp = Tree(); tp.feed(m.group(0))
    art = tp.root.kids[0]
    page = slug or 'index'
    lines = block(art, page)

    # collapse blank runs, drop empties
    body, prev = [], None
    for ln in lines:
        ln = ln.rstrip()
        if not ln.strip():
            continue
        if ln == prev:
            continue
        body.append(ln)
        prev = ln

    desc = ''
    dm = re.search(r'<meta name="description" content="([^"]*)"', src)
    if dm: desc = html.unescape(dm.group(1)).strip()
    return page, title, desc, body

manifest_pages = []
for fname, slug, title in PAGES:
    page, title, desc, body = extract(fname, slug, title)
    manifest_pages.append({'slug': slug, 'page': page, 'title': title, 'description': desc,
                           'blocks': len(body)})
    fm = ['---', f'title: {json.dumps(title)}', f'description: {json.dumps(desc)}', '---', '']
    dest = os.path.join(OUT, f'{page}.md')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf8').write(
        '\n'.join(fm) + '\n\n'.join(body) + '\n')

json.dump(images, open(os.path.join(OUT, 'images.json'), 'w', encoding='utf8'), indent=2, ensure_ascii=False)
json.dump(manifest_pages, open(os.path.join(OUT, 'pages.json'), 'w', encoding='utf8'), indent=2, ensure_ascii=False)
print(f'pages: {len(manifest_pages)}  images: {len(images)}')
for p in manifest_pages: print(f"  {p['page']:45s} {p['blocks']:3d} blocks")
credited = sum(1 for v in images.values() if v['credit'])
print(f'images with credit parsed: {credited}/{len(images)}')
