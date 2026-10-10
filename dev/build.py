#!/usr/bin/env python3
"""Photo Tools build helper. The repo's top-level files ARE the site; this only checks, stamps and stages them.

  python3 dev/build.py check              consistency checks (run before every commit)
  python3 dev/build.py stamp              sync the in-Claude tool links and bump the offline version in sw.js
  python3 dev/build.py artifact           stage the whole site for a Claude test artifact  -> dist/site/
  python3 dev/build.py artifact --tool video-layers.html
                                          stage one tool on its own                         -> dist/<tool>/

`artifact` prints the page to publish and a files map ({published path: source path}) ready for the Artifact tool.
"""
import argparse, base64, hashlib, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
REG = json.loads((ROOT / 'dev' / 'artifacts.json').read_text())
SW = ROOT / 'sw.js'

def read(p): return (ROOT / p).read_text(encoding='utf-8')

def tool_pages():
    """Tool pages are the top-level pages with a tool switcher, in switcher order."""
    first = read('photo-frame-studio.html')
    sw_block = re.search(r'class="switch".*?</nav>', first, re.S)
    hrefs = re.findall(r'href="([\w-]+\.html)"', sw_block.group(0)) if sw_block else []
    return hrefs or sorted(p.name for p in ROOT.glob('*.html') if 'class="switch"' in p.read_text(encoding='utf-8'))

def all_pages(): return sorted(p.name for p in ROOT.glob('*.html'))

def sw_files():
    m = re.search(r"const FILES=\[(.*?)\];", SW.read_text(encoding='utf-8'), re.S)
    return re.findall(r"'([^']+)'", m.group(1))

# ---------------------------------------------------------------- check
REQUIRED_HEAD = {
    'doctype': r'^<!doctype html>',
    'charset': r'<meta charset="utf-8">',
    'viewport': r'<meta name="viewport"',
    'manifest link': r'<link rel="manifest" href="manifest.webmanifest">',
    'favicon': r'href="icons/favicon-32.png"',
    'offline registration': r"navigator\.serviceWorker\.register\('sw\.js'\)",
    'title': r'<title>[^<]+</title>',
}

def check():
    problems = []
    tools, pages, files = tool_pages(), all_pages(), sw_files()
    index = read('index.html')
    for page in pages:
        html = read(page)
        for name, pat in REQUIRED_HEAD.items():
            if name == 'title' and page in ('index.html', 'share.html') and re.search(r'<title>', html) is None:
                continue  # these two set their title further down; tolerate either way
            if not re.search(pat, html, re.I | re.M):
                problems.append(f'{page}: missing {name}')
        if page not in files:
            problems.append(f'{page}: not in sw.js FILES, so it will not work offline')
    for t in tools:
        if f'href="{t}"' not in index:
            problems.append(f'index.html: no link to {t}')
        if t not in REG['tools']:
            problems.append(f'dev/artifacts.json: no artifact link for {t}')
        sw = re.search(r'class="switch".*?</nav>', read(t), re.S)
        got = re.findall(r'href="([\w-]+\.html)"', sw.group(0)) if sw else []
        if got != tools:
            problems.append(f'{t}: tool switcher differs from the others ({", ".join(got) or "none"})')
    for f in files:
        if f != './' and not (ROOT / f).exists():
            problems.append(f'sw.js FILES lists {f}, which does not exist')
    man = json.loads(read('manifest.webmanifest'))
    for icon in man.get('icons', []):
        if not (ROOT / icon['src']).exists():
            problems.append(f'manifest.webmanifest: icon {icon["src"]} does not exist')
    expect = version_hash()
    if f"const VERSION='{expect}'" not in SW.read_text(encoding='utf-8'):
        problems.append('sw.js VERSION is out of date: run `python3 dev/build.py stamp` so phones pick up the new files')
    if art_maps_stale():
        problems.append('in-Claude tool links (const ART) differ from dev/artifacts.json: run `python3 dev/build.py stamp`')
    if problems:
        print('Problems found:'); [print('  -', p) for p in problems]; return 1
    print(f'OK: {len(pages)} pages, {len(tools)} tools, offline version {expect}')
    return 0

# ---------------------------------------------------------------- stamp
def version_hash():
    h = hashlib.sha256()
    for f in sw_files():
        if f == './': continue
        h.update(f.encode()); h.update((ROOT / f).read_bytes())
    return h.hexdigest()[:12]

ART_RE = re.compile(r"const ART=\{[^}]*\}")
def art_literal():
    return 'const ART={' + ','.join(f"'{k}':'{v}'" for k, v in REG['tools'].items()) + '}'

def art_maps_stale():
    want = art_literal()
    return any(m.group(0) != want for p in all_pages() for m in ART_RE.finditer(read(p)))

def stamp():
    want = art_literal()
    for p in all_pages():
        html = read(p)
        new = ART_RE.sub(lambda m: want, html)
        if new != html:
            (ROOT / p).write_text(new, encoding='utf-8'); print('updated tool links in', p)
    v = version_hash()  # after the link sync, since it hashes the pages
    sw = SW.read_text(encoding='utf-8')
    new = re.sub(r"const VERSION='[0-9a-f]+'", f"const VERSION='{v}'", sw)
    if new != sw:
        SW.write_text(new, encoding='utf-8'); print('sw.js VERSION ->', v)
    else:
        print('sw.js VERSION already', v)
    return 0

# ---------------------------------------------------------------- artifact
SITE_EXTRAS = ['manifest.webmanifest', 'sw.js']

def stage_file(src: Path, rel: str, out: Path, files: dict):
    """Copy one file into the staging folder. Claude artifacts don't serve .tflite, so models go as base64 .txt;
    Video Layers looks for that copy when the .tflite is missing."""
    if rel.endswith('.tflite'):
        rel += '.txt'
        dst = out / rel; dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(base64.b64encode(src.read_bytes()))
    elif rel.endswith('.md') and rel.startswith('vendor/'):
        return
    else:
        dst = out / rel; dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    files[rel] = str(dst)

def artifact(tool=None, out=None):
    if tool and tool not in all_pages():
        print('unknown page', tool); return 1
    name = Path(tool).stem if tool else 'site'
    out = Path(out) if out else DIST / name
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    files = {}
    page = tool or 'index.html'
    pages = [tool] if tool else all_pages()
    for p in pages:
        html = read(p)
        if not tool:
            # whole site: keep the switcher inside this artifact instead of jumping to the single-tool copies
            html = ART_RE.sub('const ART={}', html)
        dst = out / p; dst.write_text(html, encoding='utf-8'); files[p] = str(dst)
    rels = [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'icons').rglob('*')) if p.is_file()]
    rels += SITE_EXTRAS if not tool else ['manifest.webmanifest']
    needs_vendor = any('vendor/' in read(p) for p in pages)
    if needs_vendor:
        rels += [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'vendor').rglob('*')) if p.is_file()]
    for rel in rels:
        stage_file(ROOT / rel, rel, out, files)
    files.pop(page)
    total = sum(Path(v).stat().st_size for v in files.values()) + (out / page).stat().st_size
    big = [k for k, v in files.items() if Path(v).stat().st_size > 15 * 2**20]
    plan = {'file_path': str(out / page), 'files': files,
            'url': REG['site'] if not tool else REG['tools'].get(tool)}
    (out.parent / f'{name}.publish.json').write_text(json.dumps(plan, indent=1))
    print(f'Staged {len(files) + 1} files ({total / 2**20:.1f} MB) in {out}')
    if big: print('WARNING: over the 15 MB per-file limit:', ', '.join(big))
    print(f'Publish plan: {out.parent / (name + ".publish.json")}')
    return 0

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('check'); sub.add_parser('stamp')
    a = sub.add_parser('artifact'); a.add_argument('--tool'); a.add_argument('--out')
    args = ap.parse_args()
    sys.exit({'check': check, 'stamp': stamp}.get(args.cmd, lambda: artifact(args.tool, args.out))())
