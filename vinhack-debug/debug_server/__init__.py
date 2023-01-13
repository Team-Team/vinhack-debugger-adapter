from flask import Flask
import json
app = Flask(__name__)
file = None
message = "Debug adapter not started"
source_code = ""

@app.route("/")
def home():
    return message

@app.route("/source", methods=["GET"])
def source():
    return source_code

def start_debug_adapter(file_path):
    global file, message, source_code
    file = open(file_path, "r")
    message = "Not Initilized"
    source_code = file.read()
    file.close()
    if not file: message = "Wasn't able to open file"
    app.run()

