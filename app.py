from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def postNgrokAddress():
    if request.method == "GET":
        if readAddr() == "":
            return "Fatal: ngrok address is not provided yet."
        return readAddr()
    elif request.method == "POST":
        if not request.form["addr"]:
            return "Fatal: requested field 'addr' is not provided."
        writeAddr(request.form["addr"])
        return "Success"

def writeAddr(addr):
    with open("./addr", "w") as f:
        f.write(addr)
        return True
    
def readAddr():
    addr = ""
    with open("./addr") as f:
        addr = f.read()
    return addr

if __name__ == "__main__":
	app.run()
