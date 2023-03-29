from app import db
from app.auth import token_auth
from app.decorators import paginated_response
from app.errors import bad_request
from app.models import Prompter, Story
from flask import abort, Blueprint, jsonify, request, url_for

stories = Blueprint('stories', __name__)

@stories.route('/stories', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Story, endpoint='stories.get_stories')
def get_stories():
    return db.session.query(Story), None

@stories.route('/stories', methods=['POST'])
@token_auth.login_required
def create_story():
    prompter = token_auth.current_user()
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title field')
    story = Story(prompter=prompter)
    story.from_dict(data)
    db.session.add(story)
    db.session.commit()
    response = jsonify(story.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('stories.get_story', id=story.id)
    return response

@stories.route('/stories/<int:id>', methods=['GET'])
@token_auth.login_required
def get_story(id):
    story = db.session.get(Story, id) or abort(404)
    return jsonify(story.to_dict())

@stories.route('/stories/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_story(id):
    story = db.session.get(Story, id) or abort(404)
    if story.prompter != token_auth.current_user():
        abort(403)
    data = request.get_json() or {}
    if 'title' in data and data['title'] != story.title and \
            db.session.query(Story).filter_by(title=data['title']).first():
        return bad_request('please use a different title')
    story.from_dict(data)
    db.session.commit()
    return jsonify(story.to_dict())

@stories.route('/stories/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_story(id):
    story = db.session.get(Story, id) or abort(404)
    if story.prompter != token_auth.current_user():
        abort(403)
    db.session.delete(story)
    db.session.commit()
    return '', 204

@stories.route('/stories/<int:id>/likers', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Prompter, endpoint='stories.get_likers')
def get_likers(id):
    story = db.session.get(Story, id) or abort(404)
    return story.likers, id