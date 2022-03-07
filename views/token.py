from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request

from models import User
import flask_jwt_extended
from flask import Response, request, jsonify, make_response, redirect
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta



class AccessTokenEndpoint(Resource):

    def post(self):
        body = request.get_json() or {}

        username = body.get('username')
        password = body.get('password')

        user = User.query.filter_by(username=username).first()
        print(user, username)

        if user is None:
            return Response(json.dumps({"message": "Bad username"}), mimetype="application/json", status=401)

        if user.check_password(password):
            # check username and log in credentials. If valid, return tokens

            access_token = flask_jwt_extended.create_access_token(identity=user.id)
            refresh_token = flask_jwt_extended.create_refresh_token(identity=user.id)

            resp = Response(json.dumps({
                'access_token': access_token,
                'refresh_token': refresh_token,


            }), mimetype="application/json",  status=200)

            flask_jwt_extended.set_access_cookies(resp, access_token)
            flask_jwt_extended.set_refresh_cookies(resp, refresh_token)

            return resp

        else:
            return Response(json.dumps({"message": "Bad password"}), mimetype="application/json", status=401)


class RefreshTokenEndpoint(Resource):

    # @flask_jwt_extended.jwt_required()
    def post(self):

        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        print(refresh_token)
        '''
        https://flask-jwt-extended.readthedocs.io/en/latest/refreshing_tokens/
        Hint: To decode the refresh token and see if it expired:
        decoded_token = flask_jwt_extended.decode_token(refresh_token)
        exp_timestamp = decoded_token.get("exp")
        current_timestamp = datetime.timestamp(datetime.now(timezone.utc))
        if current_timestamp > exp_timestamp:
            # token has expired:
            return Response(json.dumps({ 
                    "message": "refresh_token has expired"
                }), mimetype="application/json", status=401)
        else:
            # issue new token:
            return Response(json.dumps({ 
                    "access_token": "new access token goes here"
                }), mimetype="application/json", status=200)
        '''
        decoded_token = flask_jwt_extended.decode_token(refresh_token)
        exp_timestamp = decoded_token.get("exp")
        current_timestamp = datetime.timestamp(datetime.now(timezone.utc))

        if current_timestamp > exp_timestamp:
            # token has expired:
            return Response(json.dumps({
                "message": "refresh_token has expired"
            }), mimetype="application/json", status=401)
        else:
            # current_user = get_jwt_identity()
            access_token = flask_jwt_extended.create_access_token(12)

            # csrf = flask_jwt_extended.get_csrf_token()
            #     #request.cookies.get('csrf_access_token')

            resp = Response(json.dumps({
                'access_token': access_token,
                "csrf_request": request.cookies.get('csrf_access_token')
            }),
                mimetype="application/json", status=200)

            # flask_jwt_extended.set_access_cookies(resp, access_token)

            # issue new token:
            return resp



def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )