from flask import Response
from flask_restful import Resource
from models import LikePost, db, Post, User, Following
import json
from . import can_view_post

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self, post_id):

        following = Following.query.filter_by(user_id=self.current_user.id).all()
        user_ids = [fol.to_dict_following()["following"]["id"] for fol in following]
        user_ids.append(self.current_user.id)

        allowed_posts = Post.query.filter(Post.user_id.in_(user_ids)).all()
        allowed_posts_id = [p.to_dict()["id"] for p in allowed_posts]

        engine = db.engine
        session = db.session

        if not str(post_id).isnumeric():
            return Response(json.dumps({'message': ''}),  mimetype="application/json", status=400)
        #
        if not (int(post_id) in allowed_posts_id):
            return Response(json.dumps({'message': ''}), mimetype="application/json", status=404)

        new_like = LikePost(post_id=post_id, user_id=self.current_user.id)

        try:
            db.session.add(new_like)
            db.session.commit()

        except Exception as e:
            print(e)
            return Response(json.dumps(new_like.to_dict()), mimetype="application/json", status=400)

        return Response(json.dumps(new_like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, post_id, id):

        if not str(id).isnumeric():
            return Response(json.dumps({'message': 'Invalid ID'}), mimetype="application/json", status=400)

        post_likes = LikePost.query.filter_by(post_id=post_id, id=id, user_id=self.current_user.id).all()

        if not post_likes:
            return Response(json.dumps({}), mimetype="application/json", status=404)

        post_like = post_likes[0]

        try:
            db.session.delete(post_like)
            db.session.commit()
        except Exception as e:
            print(e)
            return Response(json.dumps({}), mimetype="application/json", status=404)

        return Response(json.dumps({}), mimetype="application/json", status=200)



        return Response(json.dumps({}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
