"""Isolated Chrome regression runner; no provider calls and no real learner storage."""
import argparse
import html
import json
from jsonschema import Draft202012Validator, FormatChecker
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from mythos_server import Handler


class QuietHandler(Handler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chrome', help='Path to Chrome/Chromium executable')
    args = parser.parse_args()
    candidates = [args.chrome, shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chrome'), r'C:\Program Files\Google\Chrome\Application\chrome.exe']
    chrome = next((candidate for candidate in candidates if candidate and Path(candidate).exists()), None)
    if not chrome:
        parser.error('Chrome not found. Supply --chrome or run the test pages on an isolated local server.')
    server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        # Do not read .env or spend money on a hosted provider during a browser test.
        with patch.dict(os.environ, {'MYTHOS_LLM_PROVIDER': ''}):
            for page, budget in [('progression.html', 10000), ('browser-smoke.html', 180000)]:
                with tempfile.TemporaryDirectory(prefix='mythos-browser-') as profile:
                    command = [chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-extensions', '--enable-logging=stderr', '--log-level=0', f'--user-data-dir={profile}', f'--virtual-time-budget={budget}', '--dump-dom', f'http://127.0.0.1:{server.server_port}/tests/{page}']
                    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=240)
                    dom = completed.stdout.decode('utf-8', errors='replace')
                    status = re.search(r'<h1 id="result"[^>]*>(.*?)</h1>', dom, re.S)
                    detail = re.search(r'<pre id="details"[^>]*>(.*?)</pre>', dom, re.S)
                    message = html.unescape(detail[1]) if detail else 'No details'
                    errors = [line for line in completed.stderr.decode('utf-8', errors='replace').splitlines() if ':CONSOLE' in line and ('ERROR' in line or 'Uncaught' in line)]
                    print(f'{page}: {status[1] if status else "NO RESULT"} {message}')
                    if completed.returncode or not status or status[1] != 'PASS' or errors:
                        raise SystemExit('\n'.join(errors) or f'Browser regression failed: {page}')
                    if page == 'browser-smoke.html':
                        snapshot = re.search(r'<pre id="progressSnapshot"[^>]*>(.*?)</pre>', dom, re.S)
                        if not snapshot:
                            raise SystemExit('Missing persisted progress snapshot')
                        schema = json.loads((Path(__file__).resolve().parents[1] / 'data/schemas/progress.schema.json').read_text(encoding='utf-8'))
                        Draft202012Validator(schema, format_checker=FormatChecker()).validate(json.loads(html.unescape(snapshot[1])))
                        print('Persisted progress schema: PASS')
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
