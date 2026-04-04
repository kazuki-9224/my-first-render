from flask import Flask, request
import os

app = Flask(__name__)

# --- ここに「正解」のデータを置いておく ---
VALID_USER = "admin"
VALID_PASS = "1234"

@app.route('/')
def home():
    return "Login API is Running!"  # サイトにアクセスした時に出る文字

# --- ここが重要！「/login」という判定窓口を作る ---
@app.route('/login', methods=['POST'])
def login_check():
    # PC側の requests.post から送られてくるデータを受け取る
    user = request.form.get("user")
    password = request.form.get("pass")

    # 判定する（お馴染みの if 文！）
    if user == VALID_USER and password == VALID_PASS:
        return "success"  # 合っていたら「success」という文字だけを返す
    else:
        return "fail"     # 違ったら「fail」という文字だけを返す

if __name__ == "__main__":
    # Renderで動かすための設定
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
