#!/usr/bin/env python3
"""Photo Tools smoke test: opens every page in headless Chromium and reports anything broken.

  python3 dev/test.py                 test the site as it is in the repo (like GitHub Pages)
  python3 dev/test.py --artifact      test the staged Claude copy in dist/site/ (run `dev/build.py artifact` first)
  python3 dev/test.py --pages video-layers.html chat-reel.html
  python3 dev/test.py --shots         also save screenshots to dist/shots/

Each page is opened on a desktop and a phone screen, both on its own and inside a frame (the way Claude shows
artifacts). It fails on script errors, missing files, sideways scrolling on phones, a tool switcher that leaves
the site, and (Video Layers) background-remover models that don't load.
Needs Python Playwright; Chromium comes from PLAYWRIGHT_BROWSERS_PATH or /opt/pw-browsers.
"""
import argparse, functools, http.server, json, mimetypes, os, re, sys, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'dev'))
import build  # noqa: E402

for ext, t in {'.webmanifest': 'application/manifest+json', '.mjs': 'text/javascript',
               '.wasm': 'application/wasm', '.js': 'text/javascript'}.items():
    mimetypes.add_type(t, ext)

VIEWPORTS = {'desktop': (1280, 800), 'phone': (390, 844)}
OFFSITE_OK = ('fonts.googleapis.com', 'fonts.gstatic.com')  # fonts may be unreachable in a sandbox; pages fall back

class Quiet(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.webmanifest': 'application/manifest+json', '.mjs': 'text/javascript', '.wasm': 'application/wasm'}
    def log_message(self, *a): pass

def serve(directory):
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(directory)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f'http://localhost:{srv.server_address[1]}/'

FRAME = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>html,body,iframe{margin:0;border:0;width:100%;height:100%}</style>' \
        '<iframe id="f" src="{src}"></iframe>'

def run(args):
    from playwright.sync_api import sync_playwright
    site = ROOT / 'dist' / 'site' if args.artifact else ROOT
    if args.artifact and not (site / 'index.html').exists():
        print('No staged copy: run `python3 dev/build.py artifact` first'); return 2
    srv, base = serve(site)
    # the frame host lives on a different origin, like claude.ai around an artifact
    host_dir = ROOT / 'dist' / '_frame'; host_dir.mkdir(parents=True, exist_ok=True)
    hsrv, hbase = serve(host_dir)
    hbase = hbase.replace('localhost', '127.0.0.1')
    pages = args.pages or build.all_pages()
    tools = set(build.tool_pages())
    shots = ROOT / 'dist' / 'shots'
    if args.shots: shots.mkdir(parents=True, exist_ok=True)
    failures, runs = [], 0
    exe = None
    for cand in [os.environ.get('PLAYWRIGHT_BROWSERS_PATH', ''), '/opt/pw-browsers']:
        p = Path(cand) / 'chromium' if cand else None
        if p and p.is_file(): exe = str(p); break
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**({'executable_path': exe} if exe else {}))
        for page_name in pages:
            for vp_name, (w, h) in VIEWPORTS.items():
                for framed in (False, True):
                    runs += 1
                    label = f'{page_name} [{vp_name}{", framed" if framed else ""}]'
                    errs = check_page(browser, base, hbase, host_dir, page_name, w, h, framed,
                                      page_name in tools, args, shots, label)
                    print(('FAIL ' if errs else 'ok   ') + label)
                    for e in errs: print('       -', e)
                    failures += [f'{label}: {e}' for e in errs]
        browser.close()
    srv.shutdown(); hsrv.shutdown()
    print(f'\n{runs - len({f.split(": ")[0] for f in failures})}/{runs} page runs clean')
    return 1 if failures else 0

def check_page(browser, base, hbase, host_dir, name, w, h, framed, is_tool, args, shots, label):
    errs = []
    ctx = browser.new_context(viewport={'width': w, 'height': h}, is_mobile=(w < 600), has_touch=(w < 600))
    ctx.route(re.compile(r'https://fonts\.(googleapis|gstatic)\.com/.*'), lambda r: r.abort())
    page = ctx.new_page()
    def on_console(m):
        if m.type != 'error': return
        url = (m.location or {}).get('url', '')
        if any(d in url for d in OFFSITE_OK) or 'fonts.g' in m.text: return
        if 'Failed to load resource' in m.text and url.endswith('.tflite'): return  # expected in artifact mode
        errs.append(f'console: {m.text[:200]}')
    page.on('console', on_console)
    page.on('pageerror', lambda e: errs.append(f'script error: {str(e)[:200]}'))
    def on_response(r):
        if r.status >= 400 and r.url.startswith(base) and not (args.artifact and r.url.endswith('.tflite')):
            errs.append(f'{r.status} for {r.url[len(base):]}')
    page.on('response', on_response)
    try:
        if framed:
            (host_dir / 'frame.html').write_text(FRAME.replace('{src}', base + name))
            page.goto(hbase + 'frame.html', wait_until='load')
            frame = None
            for _ in range(50):
                frame = next((f for f in page.frames if f.url.startswith(base + name)), None)
                if frame: break
                page.wait_for_timeout(100)
            if not frame: return errs + ['page never loaded inside the frame']
            target = frame
        else:
            page.goto(base + name, wait_until='load'); target = page
        page.wait_for_timeout(args.settle)
        if w < 600:
            # compare with the real screen width: phone Chrome zooms out to fit wide pages, so innerWidth grows too
            over = target.evaluate('document.documentElement.scrollWidth') - w
            if over > 1: errs.append(f'scrolls sideways on a phone by {over}px')
        if is_tool and framed and not args.no_switch:
            errs += check_switch(page, target, base, name)
        if name == 'video-layers.html' and vp_name_is_desktop(w) and not framed:
            errs += check_models(target)
        if args.shots:
            page.screenshot(path=str(shots / (re.sub(r'[^\w]+', '_', label).strip('_') + '.png')))
    except Exception as e:
        errs.append(f'test crashed: {str(e).splitlines()[0][:200]}')
    finally:
        ctx.close()
    return errs

def vp_name_is_desktop(w): return w >= 600

def check_switch(page, frame, base, name):
    """Inside a frame, clicking another tool should stay in this site (whole-site artifact) or open the single-tool
    artifact in a new tab (repo copy). It must never load a missing page."""
    links = frame.eval_on_selector_all('.switch a', 'as=>as.map(a=>({h:a.getAttribute("href"),u:a.href,t:a.target,c:a.getAttribute("aria-current")}))')
    others = [l for l in links if not l['c']]
    if not others: return ['tool switcher has no other tools']
    errs = []
    for l in others:
        if l['u'].startswith('https://claude.ai/artifact/'):
            if l['t'] != '_blank': errs.append(f'switcher link to {l["h"]} (a Claude artifact) does not open a new tab')
        elif not l['u'].startswith(base):
            errs.append(f'switcher link to {l["h"]} leaves the site: {l["u"]}')
    local = [l for l in others if l['u'].startswith(base)]
    if errs or not local: return errs
    other = local[0]
    frame.click(f'.switch a[href="{other["h"]}"]')
    for _ in range(50):
        f = next((f for f in page.frames if f.url.startswith(base + other['h'])), None)
        if f: return []
        page.wait_for_timeout(100)
    return [f'switching to {other["h"]} did not load it']

def check_models(target):
    """Load each background-remover model through the page's own loader (falls back to .txt copies in artifacts)."""
    res = target.evaluate('''async()=>{const out={};for(const p of Object.keys(CUT_SIZE)){if(!p.startsWith('models/'))continue;
        try{const b=await cutGet(p);out[p]=[b.byteLength??b.length,CUT_SIZE[p]];}catch(e){out[p]=String(e);}}return out;}''')
    errs = []
    for p, r in res.items():
        if not isinstance(r, list): errs.append(f'model {p} failed: {r}')
        elif r[0] != r[1]: errs.append(f'model {p} is {r[0]} bytes, expected {r[1]}')
    return errs

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--artifact', action='store_true', help='test dist/site/ instead of the repo')
    ap.add_argument('--pages', nargs='*', help='only these pages')
    ap.add_argument('--shots', action='store_true', help='save screenshots to dist/shots/')
    ap.add_argument('--settle', type=int, default=1200, help='ms to wait after load (default 1200)')
    ap.add_argument('--no-switch', action='store_true', help='skip the tool-switcher click test')
    sys.exit(run(ap.parse_args()))
