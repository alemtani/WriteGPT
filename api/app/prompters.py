from app import db
from app.auth import token_auth
from app.errors import bad_request
from app.models import Prompter, Work
from flask import abort, Blueprint, jsonify, request, url_for

prompters = Blueprint('prompters', __name__)

@prompters.route('/prompters', methods=['GET'])
@token_auth.login_required
def get_prompters():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(db.session.query(Prompter), page, per_page, 'prompters.get_prompters')
    return jsonify(data)

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
    prompter.from_dict(data, new_prompter=True)
    db.session.add(prompter)
    db.session.commit()
    response = jsonify(prompter.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('prompters.get_prompter', id=prompter.id)
    return prompter

@prompters.route('/prompters/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_prompter(user_id):
    return jsonify(db.session.query(Prompter).get_or_404(user_id).to_dict())

@prompters.route('/prompters/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def update_prompter(user_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != prompter.username and \
            db.session.query(Prompter).filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != prompter.email and \
            db.session.query(Prompter).filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    prompter.from_dict(data, new_prompter=False)
    db.session.commit()
    return jsonify(prompter.to_dict())

@prompters.route('/prompters/<int:user_id>/works', methods=['GET'])
@token_auth.login_required
def get_prompter_works(user_id):
    prompter = db.session.query(Prompter).get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection.dict(prompter.works, page, per_page, 'prompters.get_prompter_works')
    return jsonify(data)

@prompters.route('/prompters/<int:user_id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(user_id):
    prompter = db.session.query(Prompter).get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.followers, page, per_page, 'prompters.get_followers')
    return jsonify(data)

@prompters.route('/prompters/<int:user_id>/following', methods=['GET'])
@token_auth.login_required
def get_following(user_id):
    prompter = db.session.query(Prompter).get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.followed, page, per_page, 'prompters.get_followed')
    return jsonify(data)

@prompters.route('/prompters/<int:user_id>/following/<target_id>', methods=['POST'])
@token_auth.login_required
def follow(user_id, target_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    target = db.session.query(Prompter).get_or_404(target_id)
    if prompter.is_following(target):
        abort(409)
    prompter.follow(target)
    db.session.commit()
    return {}

@prompters.route('/prompters/<int:user_id>/following/<int:target_id>', methods=['DELETE'])
@token_auth.login_required
def unfollow(user_id, target_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    target = db.session.query(Prompter).get_or_404(target_id)
    if not prompter.is_following(target):
        abort(409)
    prompter.unfollow(target)
    db.session.commit()
    return {}

@prompters.route('/prompters/<int:user_id>/liked', methods=['GET'])
@token_auth.login_required
def get_liked(user_id):
    prompter = db.session.query(Prompter).get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.liked, page, per_page, 'prompters.get_liked')
    return jsonify(data)

@prompters.route('/prompters/<int:user_id>/liked/<int:target_id>', methods=['POST'])
@token_auth.login_required
def like(user_id, target_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    target = db.session.query(Work).get_or_404(target_id)
    if prompter.is_liking(target):
        abort(409)
    prompter.like(target)
    db.session.commit()
    return {}

@prompters.route('/prompters/<int:user_id>/liked/<int:target_id>', methods=['DELETE'])
@token_auth.login_required
def unlike(user_id, target_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    target = db.session.query(Work).get_or_404(target_id)
    if not prompter.is_liking(target):
        abort(409)
    prompter.unlike(target)
    db.session.commit()
    return {}

@prompters.route('/prompters/<int:user_id>/feed', methods=['GET'])
@token_auth.login_required
def get_feed(user_id):
    if token_auth.current_user().id != user_id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.get_followed_works(), page, per_page, 'prompters.get_feed')
    return jsonify(data)
