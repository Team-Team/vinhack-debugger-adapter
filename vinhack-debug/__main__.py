import git
import os
import sys


ui_github_repo_link = "https://github.com/Team-Team/vinhack-debugger-build.git"

module_directory = __file__[:-len("/__main__.py")]
ui_directory = os.path.join(module_directory ,"ui")
if not os.path.isdir(ui_directory):
    print("UI Directory is not cloned\nCloning UI Directory...")
    os.mkdir(ui_directory)
    git.Git(ui_directory).clone(ui_github_repo_link)
    print("UI Directory Cloned")

import http.server
import socketserver
from os import path
import asyncio

my_host_name = 'localhost'
my_port = 8000
my_html_folder_path = os.path.join(ui_directory, "vinhack-debugger-build") 

my_home_page_file_path = 'index.html'


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


my_handler = MyHttpRequestHandler
with socketserver.TCPServer(("", my_port), my_handler) as httpd:
    print("Http Server Serving at port", my_port)
    httpd.serve_forever()

