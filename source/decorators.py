#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from flask import abort, request
import jwt
from config import app
from provider import DataProvider


def get_token(request):
    return request.headers.get('Authorization').split('Bearer ')[1]


def tiene_jwt(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.has_key('Authorization'):
            try:

                # Pido el token del request
                token = get_token(request)
                # Traigo el payload del token
                payload = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
                # Pido las carreras del request
                carreras_str = request.args.get('carreras')
                carreras = carreras_str.split(',') if carreras_str else []
                # Chequeo que las carreras pedidas sean un subset de sus permisos
                if not set(carreras) <= set(payload['carreras']):
                    abort(401, 'El token es invalido')
            except:
                abort(401, 'El token es invalido')
        else:
            abort(401, 'Se necesita un token')
        return f(*args, **kwargs)
    return decorated_function
    