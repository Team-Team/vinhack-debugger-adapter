from flask import Flask
from flask_cors import CORS
import json
import re
import subprocess

app = Flask(__name__)
CORS(app)
pdb_shell = None
line_number = 0
file = None
message = "Debug adapter not started"
source_code = ""
file_path = ""

@app.route("/initialize")
def pdb_init():
    global pdb_shell, message, line_number
    pdb_shell = subprocess.Popen(["python", "-m", "pdb", file_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    info = pdb_shell.stdout.read(1).decode()
    while not re.search("\(Pdb\)", info):
        info += pdb_shell.stdout.read(1).decode()
    line_number = int(re.search("\((\d+)\)", info).group()[1:-1])
    message = "Initialized" 
    return message

@app.route("/")
def home():
    return message

@app.route("/linenumber")
def getLineNumber():
    return str(line_number)

@app.route("/next")
def next_line():
    global line_number
    pdb_shell.stdin.write(b"n\n")
    pdb_shell.stdin.flush()
    info = pdb_shell.stdout.read(1).decode()
    output = ""
    while not re.search("\(\d+\)<module>\(\)", info):
        char = pdb_shell.stdout.read(1).decode()
        if char == '\n':
            if re.search("\(Pdb\)", info):
                output += info[5::]
            info = ""
        else: info += char
    line_number = int(re.search("\((\d+)\)", info).group()[1:-1])
    response = {"output": output, "linenumber": line_number}
    return json.dumps(response) 

@app.route("/source", methods=["GET"])
def source():
    return source_code

def start_debug_adapter(_file_path):
    global file, message, source_code,file_path
    file_path = _file_path
    file = open(file_path, "r")
    message = "Not Initilized"
    source_code = file.read()
    file.close()
    if not file: message = "Wasn't able to open file"
    app.run()

