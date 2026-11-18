# Serveur local imitant Netlify : index.html des dossiers, _redirects (301), _headers (dont CSP), 404.html
import http.server, os, re, sys, urllib.parse
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

def load_rules():
    red = []
    for line in open(os.path.join(ROOT, '_redirects')):
        line = line.split('#')[0].strip()
        if not line: continue
        parts = line.split()
        red.append((parts[0], parts[1], parts[2].rstrip('!') if len(parts) > 2 else '301'))
    hdr, cur = [], None
    for line in open(os.path.join(ROOT, '_headers')):
        if not line.strip(): continue
        if not line.startswith(' '):
            cur = (line.strip(), []); hdr.append(cur)
        else:
            k, v = line.strip().split(':', 1); cur[1].append((k.strip(), v.strip()))
    return red, hdr
REDIRECTS, HEADERS = load_rules()

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
    def _headers_for(self, path):
        out = []
        for pat, hs in HEADERS:
            rx = '^' + re.escape(pat).replace(r'\*', '.*') + '$'
            if re.match(rx, path): out += hs
        return out
    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        for src, dst, code in REDIRECTS:
            if src == path and code in ('301', '302'):
                self.send_response(int(code)); self.send_header('Location', dst); self.end_headers(); return
        fs = os.path.join(ROOT, path.lstrip('/'))
        if os.path.isdir(fs):
            if not path.endswith('/'):
                self.send_response(301); self.send_header('Location', path + '/'); self.end_headers(); return
            fs = os.path.join(fs, 'index.html')
        if not os.path.isfile(fs):
            self.send_response(404)
            for k, v in self._headers_for(path): self.send_header(k, v)
            body = open(os.path.join(ROOT, '404.html'), 'rb').read()
            self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body); return
        self.extra = self._headers_for(path)
        self.path = urllib.parse.quote('/' + os.path.relpath(fs, ROOT))
        super().do_GET()
    def end_headers(self):
        for k, v in getattr(self, 'extra', []): self.send_header(k, v)
        self.extra = []
        super().end_headers()

http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
