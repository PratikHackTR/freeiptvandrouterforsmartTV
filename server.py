import os
import sys
import json
import socket
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = 9901
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEDEF_FILE = os.path.join(BASE_DIR, "hedef.txt")
CHANNELS_FILE = os.path.join(BASE_DIR, "channels.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")

def get_local_ip():
    """Gets local IP address of the machine on local network."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def read_hedef_url():
    """Reads target URL from hedef.txt."""
    if os.path.exists(HEDEF_FILE):
        try:
            with open(HEDEF_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                if lines:
                    url = lines[0]
                    if not url.startswith("http://") and not url.startswith("https://"):
                        url = "https://" + url
                    return url
        except Exception as e:
            print(f"[!] Error reading hedef.txt: {e}")
    return "https://www.youtube.com"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True

class PHTVRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path).path

        # 1. Main Landing Page
        if parsed_path == "/" or parsed_path == "/index.html":
            return self.serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")

        # 2. Canli TV Player Page
        elif parsed_path == "/tv" or parsed_path == "/tv.html":
            return self.serve_file(os.path.join(STATIC_DIR, "tv.html"), "text/html; charset=utf-8")

        # 3. Yönlendir (Redirect) Endpoint
        elif parsed_path == "/redirect":
            target_url = read_hedef_url()
            print(f"[-->] Redirecting client to: {target_url}")
            self.send_response(302)
            self.send_header("Location", target_url)
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            
            # HTML Fallback for TV Browsers that don't auto-follow 302
            fallback_html = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="refresh" content="0;url={target_url}">
                <title>Yönlendiriliyor...</title>
            </head>
            <body style="background:#0f172a;color:#fff;font-family:sans-serif;text-align:center;padding-top:20%;">
                <h2>Yönlendiriliyorsunuz...</h2>
                <p><a href="{target_url}" style="color:#38bdf8;">Tıklayın (Eğer otomatik gitmezse)</a></p>
                <script>window.location.href = "{target_url}";</script>
            </body>
            </html>"""
            self.wfile.write(fallback_html.encode('utf-8'))
            return

        # 4. API: Channel Catalog
        elif parsed_path == "/api/channels":
            channels_json = "[]"
            if os.path.exists(CHANNELS_FILE):
                try:
                    with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
                        channels_json = f.read()
                except Exception as e:
                    print(f"[!] Error reading channels.json: {e}")
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(channels_json.encode('utf-8'))
            return

        # 5. API: System Info (Local IP & Target URL)
        elif parsed_path == "/api/info":
            info_data = {
                "local_ip": get_local_ip(),
                "target_url": read_hedef_url(),
                "port": PORT
            }
            response_bytes = json.dumps(info_data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_bytes)
            return

        # 6. Static files fallback
        else:
            rel_path = parsed_path.lstrip("/")
            file_path = os.path.join(STATIC_DIR, rel_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                content_type = self.guess_type(file_path)
                return self.serve_file(file_path, content_type)
            else:
                self.send_error(404, "Dosya Bulunamadi")

    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"[!] File serve error: {e}")
            self.send_error(500, "Sunucu hatasi")

    def log_message(self, format, *args):
        # Clean custom logger
        print(f"[PHTV Server] {self.address_string()} - {format % args}")

def run_server():
    local_ip = get_local_ip()
    print("=" * 60)
    print("        PHTV LOCALHOST 9901 MEDIA SERVER RUNNING          ")
    print("=" * 60)
    print(f" [*] Bilgisayar Yerel Adres: http://localhost:{PORT}")
    print(f" [*] TV Web Tarayıcısı İle Erişim: http://{local_ip}:{PORT}")
    print(f" [*] Yönlendir Hedef Dosyası: {HEDEF_FILE}")
    print(f" [*] Yönlendir Hedef URL   : {read_hedef_url()}")
    print("=" * 60)
    print("Durdurmak için Ctrl+C tuşlarına basabilirsiniz.\n")

    server_address = ("0.0.0.0", PORT)
    httpd = ThreadedHTTPServer(server_address, PHTVRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Sunucu kapatılıyor...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
