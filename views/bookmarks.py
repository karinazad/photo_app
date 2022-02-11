from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from . import can_view_post, post_exists, handle_db_insert_error


class BookmarksListEndpoint(Resource):
    # List all bookmarks and create bookmars

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # Your code here
        # Show bookmarks associated with the current used
        # 1. Use SQL Alchemy and json serialize

        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        # print(bookmarks)
        bookmarks_list_of_dictionaries = [
            bookmark.to_dict() for bookmark in bookmarks
        ]
        return Response(json.dumps(bookmarks_list_of_dictionaries), mimetype="application/json", status=200)

    @handle_db_insert_error
    def post(self):
        body = request.get_json()

        post_id = body.get("post_id")

        if not post_exists(post_id):
            message = f'Post does not exist.'
            response_obj = {
                'message': message
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)

        if type(post_id) is not int:
            message = f'Invalid Post ID format provided: {post_id}. Must be a number'
            response_obj = {
                'message': message
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)

        if not can_view_post(user=self.current_user, post_id=post_id):
            message = 'You are not authorized to do this.'
            response_obj = {
                'message': message
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)

        bookmark = Bookmark(user_id=self.current_user.id, post_id=post_id)

        db.session.add(bookmark)
        db.session.commit()

        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)


class BookmarkDetailEndpoint(Resource):

    # Patch (updating), get individual bookmarks, delete bookmarks

    def __init__(self, current_user):
        self.current_user = current_user

    def delete(self, id):
        try:
            int_id = int(id)
        except:
            response_obj = {
                    'message': "Invalid id format provided."
                }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)

        db_bookmarks = Bookmark.query.filter_by(id=id).all()

        if len(db_bookmarks) == 0:
            response_obj = {
                'message': "No bookmarks found"
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)

        bookmarks = [
            bookmark.to_dict() for bookmark in db_bookmarks
        ]

        bookmarks = bookmarks[0]
        post_id = bookmarks["post"]["id"]

        if not can_view_post(user=self.current_user, post_id=post_id):
            message = 'You are not authorized to do this.'
            response_obj = {
                'message': message
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)

        try:
            db.session.delete(db_bookmarks[0])
            db.session.commit()
        except Exception as e:
            print(e)

        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint,
        '/api/bookmarks',
        '/api/bookmarks/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint,
        '/api/bookmarks/<id>',
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
