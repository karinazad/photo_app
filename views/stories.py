from flask import Response
from flask_restful import Resource
from models import Story, Following, db
from . import get_authorized_user_ids
import json

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        engine = db.engine
        session = db.session

        user_ids_tuples = (
            session
                .query(Following.following_id)
                .filter(Following.user_id == self.current_user.id)
                .order_by(Following.following_id)
                .all()
        )
        user_ids = [id for (id,) in user_ids_tuples]

        user_ids.append(self.current_user.id)

        stories = Story.query.all()
        stories = [s.to_dict() for s in stories]

        correct_stories = []

        for story in stories:
            if story["user"]["id"] in user_ids:
                correct_stories.append(story)

        return Response(json.dumps(correct_stories), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
