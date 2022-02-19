from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from . import handle_db_insert_error, can_view_post


def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here

        following = Following.query.filter_by(user_id=self.current_user.id).all()
        following = [fol.to_dict_following() for fol in following]

        return Response(json.dumps(following), mimetype="application/json", status=200)

    def post(self):
        # Your code here

        all_users = User.query.all()
        all_users_id = [user.to_dict()["id"] for user in all_users]

        body = request.get_json()

        user_id = body.get('user_id')

        if not user_id:
            return Response(json.dumps({'message': 'Invalid or no user id provided'}),
                            mimetype="application/json", status=400)

        if not str(user_id).isnumeric():
            return Response(json.dumps({'message': 'Invalid or no user id provided'}),
                            mimetype="application/json", status=400)

        # if user_id not in all_users_id:
        #     return Response(json.dumps({'message': 'Invalid or no user id provided'}),
        #              mimetype="application/json", status=404)

        following = Following(user_id=self.current_user.id, following_id=user_id)

        try:
            db.session.add(following)
            db.session.commit()
        except Exception as e:
            return Response(json.dumps({'message': 'Invalid request'}), mimetype="application/json", status=400)

        following = following.to_dict_following()
        return Response(json.dumps(following), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):

        if not str(id).isnumeric():
            return Response(json.dumps({'message': 'Invalid or no user id provided'}),
                            mimetype="application/json", status=400)

        followings = Following.query.filter_by(user_id=self.current_user.id, id=id).all()

        if not followings:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        following = followings[0]

        try:
            db.session.delete(following)
            db.session.commit()
        except Exception as e:
            print(e)
            return Response(json.dumps({}), mimetype="application/json", status=404)

        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
