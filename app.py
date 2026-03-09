from flask import Flask, request, make_response, render_template
import requests

app = Flask(__name__)

FLIGHT = {"id": "KE001", "from":"Seould", "to": "Hawaii", "price" : 200000}

@app.route("/")
def index():
    return render_template("index.html", flight=FLIGHT)

@app.route("/search")
def search():
    city = request.args.get("city", "")
    coupon = request.cookies.get("coupon", "")

    resp = make_response(render_template("search.html", city=city,  flight=FLIGHT, coupon=coupon))
    resp.headers["X-Search-City"] = city
    return resp

@app.route("/buy")
def buy():
    coupon = request.cookies.get("coupon", "")
    return render_template("buy.html", flight=FLIGHT, coupon=coupon)

@app.route("/purchase", methods=["POST"])
def purchase():
    coupon = request.form.get("coupon","")

    try:
        result = requests.post(
            "http://backend:4000/internal/purchase",
            json={"flightID": FLIGHT["id"], "coupon": coupon},
            timeout=3
        )
        data = result.json()
    
    except Exception as e:
        return str(e), 500
    
    if data.get("success"):
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
        return render_template("flag.html", flag=flag)
    else:
        return data.get("message", "구매 실패"), 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)