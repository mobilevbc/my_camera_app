import flet as ft
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
            <html>
                <head><title>Mobile Camera Stream</title></head>
                <body style="margin:0; background-color:#121212; display:flex; justify-content:center; align-items:center; height:100vh;">
                    <h2 style="color:white; font-family:sans-serif;">Mobile Camera Active Stream</h2>
                </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    server = HTTPServer(('0.0.0.0', 8080), StreamHandler)
    server.serve_forever()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def main(page: ft.Page):
    page.title = "Mobile Cam Streamer"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    threading.Thread(target=start_http_server, daemon=True).start()

    ip_address = get_local_ip()
    stream_url = f"http://{ip_address}:8080/video_feed"

    page.add(
        ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, size=70, color=ft.Colors.BLUE_400),
        ft.Text("Mobile Camera Streamer", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("പൈത്തൺ & Flet ഉപയോഗിച്ച് നിർമ്മിച്ചത്", size=14, color=ft.Colors.GREY_400),
        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
        
        ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("ലാപ്‌ടോപ്പ് ബ്രൗസറിൽ നൽകേണ്ട ലിങ്ക്:", size=14, color=ft.Colors.GREY_300),
                    ft.SelectableText(stream_url, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
    )

ft.app(target=main)
