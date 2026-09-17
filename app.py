from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Docker Jenkins CI/CD Demo",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/api/users")
def users():
    return jsonify({
        "users": [
            {
                "id": 1,
                "name": "Yuvanesh"
            },
            {
                "id": 2,
                "name": "DevOps User"
            }
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)