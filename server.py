# -*- coding: utf-8 -*-
"""
AstroChat Proxy Server
Serves the HTML page and proxies /api/chat to Ollama.
"""

import http.server
import urllib.request
import urllib.error
import json
import os

PORT = 8080
OLLAMA_URL = "http://localhost:11434/api/chat"

class AstroChatHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  [{self.address_string()}] {format % args}")

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    # ── Serve static files ─────────────────────────────────────────────
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "/index.html":
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        else:
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), path.lstrip("/"))

        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            mime = "text/html" if filepath.endswith(".html") else "text/plain"
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(content))
            self._cors_headers()
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")

    # ── Proxy POST /api/chat → Ollama ───────────────────────────────────
    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                req = urllib.request.Request(
                    OLLAMA_URL,
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson")
                    self._cors_headers()
                    self.end_headers()

                    while True:
                        chunk = resp.read(512)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        self.wfile.flush()

            except urllib.error.URLError as e:
                msg = json.dumps({"error": f"Cannot reach Ollama: {str(e.reason)}"}).encode()
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self._cors_headers()
                self.end_headers()
                self.wfile.write(msg)

            except Exception as e:
                msg = json.dumps({"error": str(e)}).encode()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self._cors_headers()
                self.end_headers()
                self.wfile.write(msg)
        else:
            self.send_error(404)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print()
    print("  AstroChat Server")
    print("  " + "=" * 33)
    print(f"  Web UI  -> http://localhost:{PORT}")
    print(f"  Ollama  -> {OLLAMA_URL}")
    print("  " + "=" * 33)
    print("  Press Ctrl+C to stop")
    print()

    with http.server.ThreadingHTTPServer(("", PORT), AstroChatHandler) as httpd:
        httpd.serve_forever()
