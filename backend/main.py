from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/internal/purchase", methods=["POST"])
def purchase():
    data = request.get_json()
    coupon = data.get("coupon", "")

    if coupon == "HALF50":
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "유효한 쿠폰이 없습니다. 50% 할인 쿠폰을 먼저 획득하세요."})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)