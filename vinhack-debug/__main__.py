import git
import os
import sys
import http.server
import socketserver
from os import path
import webbrowser


ui_github_repo_link = "https://github.com/Team-Team/vinhack-debugger-build.git"
module_directory = __file__[:-len("/__main__.py")]
ui_directory = os.path.join(module_directory ,"ui")
print(ui_directory)

def clone_ui():
    if not os.path.isdir(ui_directory):
        print("UI Directory is not cloned\nCloning UI Directory...")
        os.mkdir(ui_directory)
        git.Git(ui_directory).clone(ui_github_repo_link)
        print("UI Directory Cloned")



class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', path.getsize(self.getPath()))
        self.end_headers()

    def getPath(self):
        if self.path == '/':
            content_path = path.join(
                my_html_folder_path, my_home_page_file_path)
        else:
            content_path = path.join(my_html_folder_path, str(self.path).split('?')[0][1:])
        return content_path

    def getContent(self, content_path):
        with open(content_path, mode='r', encoding='utf-8') as f:
            content = f.read()
        return bytes(content, 'utf-8')

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.getContent(self.getPath()))



def start_ui_server():
    my_host_name = 'localhost'
    my_port = 6969
    my_html_folder_path = os.path.join(ui_directory, "vinhack-debugger-build") 


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=my_html_folder_path, **kwargs)
    
    httpd = socketserver.TCPServer(("", my_port), Handler)
    webbrowser.open(f"http://127.0.0.1:{my_port}/index.html")
    httpd.serve_forever()

def run():
    clone_ui()
    start_ui_server()

run()
