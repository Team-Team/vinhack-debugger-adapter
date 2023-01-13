import git
from debug_server import start_debug_adapter
import os
import sys
import http.server
import socketserver
from os import path
import webbrowser
from threading import Thread


ui_github_repo_link = "https://github.com/Team-Team/vinhack-debugger-build.git"
module_directory = __file__[:-len("/__main__.py")]
ui_directory = os.path.join(module_directory ,"ui")

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
    my_html_folder_path = os.path.join(ui_directory, "vinhack-debugger-build") 


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=my_html_folder_path, **kwargs)
    
    httpd = socketserver.TCPServer(("", 0), Handler)
    my_port = httpd.server_address[1]
    webbrowser.open(f"http://127.0.0.1:{my_port}/index.html")
    httpd.serve_forever()

def run():
    file_path = os.path.join(os.getcwd(), sys.argv[1])
    clone_ui()
    ui_server_thread = Thread(target=start_ui_server)
    ui_server_thread.start()
    start_debug_adapter(file_path)

run()
