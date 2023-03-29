from app import db
from app.auth import token_auth
from app.decorators import paginated_response
from app.errors import bad_request
from app.models import Prompter, Story
from flask import abort, Blueprint, jsonify, request, url_for

prompters = Blueprint('prompters', __name__)

@prompters.route('/prompters', methods=['POST'])
def create_prompter():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if db.session.query(Prompter).filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if db.session.query(Prompter).filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    prompter = Prompter()
    prompter.from_dict(data)
    db.session.add(prompter)
    db.session.commit()
    response = jsonify(prompter.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('prompters.get_prompter', id=prompter.id)
    return response

@prompters.route('/prompters', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Prompter, endpoint='prompters.get_prompters')
def get_prompters():
    return db.session.query(Prompter), None

@prompters.route('/prompters/<int:id>', methods=['GET'])
@token_auth.login_required
def get_prompter(id):
    prompter = db.session.get(Prompter, id) or abort(404)
    return jsonify(prompter.to_dict())

@prompters.route('/prompters/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_prompter(id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != prompter.username and \
            db.session.query(Prompter).filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != prompter.email and \
            db.session.query(Prompter).filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    if 'password' in data and ('old_password' not in data or 
                               not prompter.check_password(data['old_password'])):
        return bad_request('must include old_password to change password')
    prompter.from_dict(data)
    db.session.commit()
    return jsonify(prompter.to_dict())

@prompters.route('/prompters/<int:id>/stories', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Story, endpoint='prompters.get_prompter_stories')
def get_prompter_stories(id):
    prompter = db.session.get(Prompter, id) or abort(404)
    return prompter.stories, id

@prompters.route('/prompters/<int:id>/followers', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Prompter, endpoint='prompters.get_followers')
def get_followers(id):
    prompter = db.session.get(Prompter, id) or abort(404)
    return prompter.followers, id

@prompters.route('/prompters/<int:id>/following', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Prompter, endpoint='prompters.get_following')
def get_following(id):
    prompter = db.session.get(Prompter, id) or abort(404)
    return prompter.followed, id

@prompters.route('/prompters/<int:id>/following/<target_id>', methods=['POST'])
@token_auth.login_required
def follow(id, target_id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    target = db.session.get(Prompter, target_id) or abort(404)
    if prompter.is_following(target):
        abort(409)
    prompter.follow(target)
    db.session.commit()
    return {}, 204

@prompters.route('/prompters/<int:id>/following/<int:target_id>', methods=['DELETE'])
@token_auth.login_required
def unfollow(id, target_id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    target = db.session.get(Prompter, target_id) or abort(404)
    if not prompter.is_following(target):
        abort(409)
    prompter.unfollow(target)
    db.session.commit()
    return {}, 204

@prompters.route('/prompters/<int:id>/liked', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Story, endpoint='prompters.get_liked')
def get_liked(id):
    prompter = db.session.get(Prompter, id) or abort(404)
    return prompter.liked, id

@prompters.route('/prompters/<int:id>/liked/<int:target_id>', methods=['POST'])
@token_auth.login_required
def like(id, target_id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    target = db.session.get(Story, target_id) or abort(404)
    if prompter.is_liking(target):
        abort(409)
    prompter.like(target)
    db.session.commit()
    return {}, 204

@prompters.route('/prompters/<int:id>/liked/<int:target_id>', methods=['DELETE'])
@token_auth.login_required
def unlike(id, target_id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    target = db.session.get(Story, target_id) or abort(404)
    if not prompter.is_liking(target):
        abort(409)
    prompter.unlike(target)
    db.session.commit()
    return {}, 204

@prompters.route('/prompters/<int:id>/feed', methods=['GET'])
@token_auth.login_required
@paginated_response(model_class=Story, endpoint='prompters.get_feed')
def get_feed(id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.get(Prompter, id) or abort(404)
    return prompter.followed_stories(), id
