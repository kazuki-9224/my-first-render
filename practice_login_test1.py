from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy # これが今回の主役！
import os

app = Flask(__name__)

# --- データベースの設定 ---
# sqliteという簡易的なDBファイル（instance/test.db）を使う設定です
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- データベースの「型（モデル）」を決める ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# 最初に1回だけ、空のデータベース（テーブル）を作る命令
with app.app_context():
    db.create_all()
    # テスト用に最初の一人だけコードで追加しておく（既にあればスキップされる）
    if not User.query.filter_by(username="admin").first():
        admin_user = User(username="admin", password="1234")
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def home():
    return "Database Login System is Running!"

# --- ログイン判定窓口 ---
@app.route('/login', methods=['POST'])
def login_check():
    user = request.form.get("user")
    password = request.form.get("pass")

    # DBの中から、そのユーザー名の人を探す
    target = User.query.filter_by(username=user).first()

    # 見つかった、かつ、パスワードが一致したら成功
    if target and target.password == password:
        return "success"
    else:
        return "fail"

# --- 【新機能！】ユーザー登録窓口 ---
@app.route('/register', methods=['POST'])
def register():
    user = request.form.get("user")
    pw = request.form.get("pass")
    
    # 既に同じ名前の人がいないかチェック
    if User.query.filter_by(username=user).first():
        return "exists"
    
    # 新しいユーザーをDBに保存（ガシャン！）
    new_user = User(username=user, password=pw)
    db.session.add(new_user)
    db.session.commit()
    return "created"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)