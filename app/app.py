from flask import Flask, request, render_template, session
from werkzeug.wrappers import Response
import os

app = Flask(__name__)
app.secret_key = "supersecretkey_fixed"

FLAG = open("flag.txt").read()

FLIGHT = {"id": "KE001", "from": "Seoul", "to": "Hawaii", "price": 200000}

ADMIN_SESSION_COOKIE = None

@app.route("/")
def index():
    return render_template("index.html", flight=FLIGHT)

@app.route("/search")
def search():
    city = request.args.get("city", "")
    html = render_template("search.html", city=city, flight=FLIGHT)

    
    resp = Response(html, status=200, mimetype='text/html')
    resp.headers._list.append(('X-Search-City', city))
    return resp

@app.route("/flag")
def flag():
    if not session.get("is_admin"):
        return "403 Forbidden: admin only", 403
    return f"<h1>{FLAG}</h1>"

@app.route("/steal")
def steal():
    stolen = request.args.get("cookie", "")
    if not stolen:
        return "no cookie", 400
    
    for part in stolen.split(";"):
        part = part.strip()
        if part.startswith("session="):
            session_val = part[len("session="):]
            if session_val == ADMIN_SESSION_COOKIE:
                return render_template("flag.html", flag=FLAG), 200

    return "invalid cookie", 403

@app.route("/internal/set-admin-cookie")
def set_admin_cookie():
    global ADMIN_SESSION_COOKIE
    if request.remote_addr != "127.0.0.1":
        return "403 Forbidden", 403
    ADMIN_SESSION_COOKIE = request.args.get("value", "")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
