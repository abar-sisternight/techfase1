from flask import jsonify
from app import app, auth

@app.route('/')
def home():
    return "Hello Anonimous user!"

@app.route('/login', methods=['GET'])
@auth.login_required #natycomments: está referenciando o auth que está em app.auth, o qual foi inicianizado com o httpbasicauth
def login():
    username = format(auth.current_user())
    return jsonify({"message": "Hello: " + username })


