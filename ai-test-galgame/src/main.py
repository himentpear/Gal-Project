import http.server
import socketserver
import webbrowser
import os
import sys

# Define the port
PORT = 8000
# Define the web directory
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web_version")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

def main():
    if not os.path.exists(WEB_DIR):
        print(f"Error: Web directory not found at {WEB_DIR}")
        return

    print(f"Starting Galgame Web Engine at http://localhost:{PORT}")
    print(f"Serving files from {WEB_DIR}")

    # Attempt to open the browser (might not work in all environments)
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        pass

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving forever. Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()

if __name__ == "__main__":
    main()
