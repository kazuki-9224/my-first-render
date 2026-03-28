from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello! Render!</h1><p>これは私の最初のサーバーです。</p>"

if __name__ == "__main__":
    # Renderではポート番号を指定する必要があるため、この書き方が安全
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)