from flask import Flask, request
app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome!"
@app.route("/get_message", methods=["GET"])
def get_message():
    message = request.args.get("message")
    return f"参数是{message}"
@app.route("/post_message", methods=["POST"])
def post_message():
    data = request.get_json()
    body = data.get("body")
    param = request.args.get("param")
    return f"body中的参数是{body},param中的参数是{param}"
if __name__ == "__main__":
    app.run(debug=True, port=5000)