import functools
from flask import abort, request
import jwt
from config import app

def tiene_jwt(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.has_key('Authorization'):
            try:
                token = request.headers.get('Authorization').split('Bearer ')[1]
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            except:
                abort(401, 'El token es inválido')
        else:
            abort(401, 'Se necesita un token')
        return f(*args, **kwargs)
    return decorated_function