import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
from models import User, Following, db
from . import get_authorized_user_ids
import json

from tests import utils

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    def get(self):

        # all_users = User.query.all()
        # all_users = [user.to_dict() for user in all_users]
        #
        # followings = Following.query.filter_by(user_id=self.current_user.id).all()
        # followings_ids = [fol.to_dict_following()["id"] for fol in followings]
        # new_users = []
        #
        # for user in all_users:
        #     if user["id"] not in followings_ids:
        #         new_users.append(user)
        #
        #     if len(new_users) == 7:
        #         break

        ids = utils.get_unrelated_users(self.current_user.id)
        new_users = User.query.filter(User.id.in_(ids)).all()

        if len(new_users) > 7:
            new_users = new_users[:7]

        new_users = [
            user.to_dict() for user in new_users
        ]

        return Response(json.dumps(new_users), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
