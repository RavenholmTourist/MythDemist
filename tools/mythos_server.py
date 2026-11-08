#!/usr/bin/env python
"""Serve Mythos and the local grounded-assistant API."""
import argparse, json, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
from mythos_assistant import answer

ROOT = Path(__file__).resolve().parents[1]

def load_env_file():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _local_request(self):
        hosts = {f'localhost:{self.server.server_port}', f'127.0.0.1:{self.server.server_port}'}
        origin = self.headers.get('Origin')
        return self.headers.get('Host', '').lower() in hosts and (origin is None or origin.lower() in {f'http://{host}' for host in hosts})

    def send_head(self):
        if not self._local_request():
            self.send_error(403)
            return None
        # Serving the repo root must never expose .env, VCS data, tools, or symlinks outside it.
        path = unquote(urlsplit(self.path).path).replace("\\", "/")
        parts = [part for part in path.split("/") if part]
        allowed = not parts or parts[0] in {"index.html", "styles.css", "src", "content", "tests"}
        target = (ROOT / path.lstrip("/")).resolve()
        resolved_parts = target.relative_to(ROOT.resolve()).parts if target.is_relative_to(ROOT.resolve()) else ()
        resolved_allowed = target == ROOT.resolve() or bool(resolved_parts and resolved_parts[0] in {'index.html', 'styles.css', 'src', 'content', 'tests'})
        if not allowed or not resolved_allowed or any(part.startswith('.') for part in [*parts, *resolved_parts]):
            self.send_error(404)
            return None
        if target.is_dir() and parts:
            self.send_error(404)
            return None
        return super().send_head()

    def _json(self, status, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        # A hostile web page must not trigger paid localhost calls via a simple cross-origin POST.
        if not self._local_request():
            self._json(403, {'error': 'Local same-origin requests only'})
            return
        if self.headers.get('Content-Type', '').split(';')[0].strip().lower() != 'application/json':
            self._json(415, {'error': 'Use application/json'})
            return
        if self.path != "/api/assistant":
            self._json(404, {"error": "Unknown endpoint"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > 16384:
                self._json(413, {"error": "Request too large"})
                return
            payload = json.loads(self.rfile.read(length) or b"{}")
            query = payload.get('query') if isinstance(payload, dict) else None
            if not isinstance(query, str) or not query.strip() or len(query) > 4000:
                self._json(400, {'error': 'Query must be nonempty text of at most 4000 characters'})
                return
            query = query.strip()
            tradition = payload.get('tradition')
            if tradition is not None and (not isinstance(tradition, str) or len(tradition) > 80):
                self._json(400, {'error': 'Invalid tradition'})
                return
            self._json(200, answer(query, tradition=tradition, lesson_id=payload.get('lessonId')))
        except ValueError:
            self._json(400, {'error': 'Invalid JSON request'})
        except Exception:
            self._json(500, {'error': 'Assistant unavailable; use local passage retrieval'})


def main():
    load_env_file()
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.getenv("MYTHOS_PORT", "4873")))
    args = parser.parse_args()
    print(f"Serving Mythos and assistant API at http://localhost:{args.port}/")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()

if __name__ == "__main__":
    main()
