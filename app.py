from flask import Flask, request
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def postNgrokAddress():
    if request.method == "GET":
        ngrokAddr = readAddr()
        if ngrokAddr == "":
            return "Fatal: ngrok address is not provided yet."
        return ngrokAddr
    elif request.method == "POST":
        if not request.form["addr"]:
            return "Fatal: requested field 'addr' is not provided."
        writeAddr(request.form["addr"])
        return "Success"

def writeAddr(addr):
    with getConnection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id from urls order by id desc limit 1")
            (id,) = cur.fetchone()
            id+=1
            cur.execute("INSERT INTO urls VALUES (%d, %s)", (id, addr))
        cur.commit()
    return True


def readAddr():
    with getConnection() as conn:
        with conn.cursor () as cur:
            cur.execute("SELECT url FROM urls ORDER BY id DESC LIMIT 1")
            addr = cur.fetchone()
            return addr
    return ""


def getConnection():
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url)
