from flask import Response, request
from flask_restful import Resource
from models import Post, User, db, Following
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here

        follower = Following.query.filter_by(following_id=self.current_user.id).all()

        follower = [fol.to_dict_follower() for fol in follower]

        return Response(json.dumps(follower), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user,
                                   # api.app.current_user
                               }
    )
