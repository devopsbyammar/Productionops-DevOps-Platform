from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0.0"
ENVIRONMENT = "production"


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ProductionOps</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 50px;
            }
            .container {
                max-width: 700px;
                margin: auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                margin-bottom: 10px;
            }
            .status {
                display: inline-block;
                padding: 8px 15px;
                background: #d4edda;
                color: #155724;
                border-radius: 5px;
                font-weight: bold;
            }
            .info {
                margin-top: 25px;
                line-height: 1.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ProductionOps Application</h1>
            <p>End-to-End DevOps Production Platform</p>

            <p class="status">APPLICATION HEALTHY</p>

            <div class="info">
                <strong>Environment:</strong> production<br>
                <strong>Version:</strong> 1.0.0<br>
                <strong>Service:</strong> productionops-web
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        version=APP_VERSION,
        environment=ENVIRONMENT
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
