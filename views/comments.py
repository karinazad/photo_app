from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post, User

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        body = request.get_json()
        post_id = body.get("post_id")
        text = body.get("text")

        all_posts = Post.query.all()
        all_posts_id = [p.to_dict()["id"] for p in all_posts]

        engine = db.engine
        session = db.session

        accessible_posts = (
            session
                .query(Post, User)
                .join(User, User.id == Post.user_id)
                .filter(Post.user_id==self.current_user.id).all()
        )
        accessible_posts = [p[0] for p in accessible_posts]
        all_accessible_posts_id = [p.to_dict()["id"] for p in accessible_posts]


        if not str(post_id).isnumeric():
            return Response(json.dumps({'message': 'Invalid or no post_id provided'}),  mimetype="application/json", status=400)

        if not post_id in all_posts_id or post_id not in all_accessible_posts_id:
            return Response(json.dumps({'message': ''}), mimetype="application/json",
                            status=404)


        comment = Comment(text=text, user_id=self.current_user.id, post_id=post_id)

        try:
            db.session.add(comment)
            db.session.commit()

        except Exception as e:
            return Response(json.dumps({'message': 'Invalid request'}), mimetype="application/json", status=400)

        comment = comment.to_dict()
        return Response(json.dumps(comment), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        if not str(id).isnumeric():
            return Response(json.dumps({'message': 'Invalid or no id provided'}),
                            mimetype="application/json", status=400)

        comment = Comment.query.filter_by(user_id=self.current_user.id, id=id).all()

        if not comment:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        comment = comment[0]

        try:
            db.session.delete(comment)
            db.session.commit()
        except Exception as e:
            print(e)
            return Response(json.dumps({}), mimetype="application/json", status=404)

        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
