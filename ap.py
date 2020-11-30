from flask import Flask, jsonify, request, make_response
from datetime import timedelta, datetime
from functools import wraps

import json
import jwt

app = Flask(__name__)

app.config["SECRET_KEY"] = "teste"

def token_required(f):
    @wraps(f)
    def decorated (*args, **kwargs):
        token = request.args.get("token")

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        
        try:
            data = jwt.decode(token, app.config ['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == "password":
        token = jwt.encode({"user" : auth.username, "exp" : datetime.utcnow() + timedelta(minutes=30)}, app.config ["SECRET_KEY"])
        return jsonify({"token" : token.decode("UTF-8")})

    return make_response('Could not verify!',401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/testAuth')
@token_required
def testAuth() -> str:
    return "Ok with authentication"

@app.route('/testNoAuth')
def testNoAuth() -> str:
    return "Ok with no authentication"