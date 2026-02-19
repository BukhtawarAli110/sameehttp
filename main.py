import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

# The default HTML content
DEFAULT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>github.com/BukhtawarAli110/sameehttp/</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
               display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f4f4f9; }
        .container { text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Samee,a web server built only for simplicity</h1>
    </div>
</body>
</html>
"""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        root = os.getcwd()
        
        # Determine the file path
        if self.path == '/':
            filename = 'index.html'
        else:
            filename = self.path.lstrip('/')

        file_path = os.path.join(root, filename)

        # 1. Check if the file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type:
                self.send_header("Content-type", content_type)
            self.end_headers()
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        
        # 2. If it's the home page and index.html is missing, show the welcome page
        elif self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(DEFAULT_PAGE, "utf-8"))
            
        # 3. Handle 404s
        else:
            self.send_error(404, "Page Not Found: %s" % self.path)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Samee started at http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Samee stopped.")
