from flask import Flask
from flask_cors import CORS
import json
import pexpect
import re

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
    pdb_shell = pexpect.spawn("pdb " + file_path)
    info = pdb_shell.readline().decode()
    line_number = int(re.search("\((\d+)\)", info).group()[1:-1])
    pdb_shell.expect("(Pdb)")
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
    pdb_shell.sendline("n")
    info = pdb_shell.readline().decode()
    output = ""
    while not re.search("\(\d+\)<module>\(\)", info):
        output += info
        info = pdb_shell.readline().decode()
    line_number = int(re.search("\((\d+)\)", info).group()[1:-1])
    pdb_shell.expect("(Pdb)")
    response = {"output": output[5::], "linenumber": line_number}
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

