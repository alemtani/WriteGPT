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

@prompters.route('/prompters/<int:id>', methods=['GET'])
@token_auth.login_required
def get_prompter(id):
    return jsonify(db.session.query(Prompter).get_or_404(id).to_dict())

@prompters.route('/prompters/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_prompter(id):
    if token_auth.current_user().id != id:
        abort(403)
    prompter = db.session.query(Prompter).get_or_404(id)
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

@prompters.route('/prompters/<int:id>/works', methods=['GET'])
@token_auth.login_required
def get_prompter_works(id):
    prompter = db.session.query(Prompter).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection.dict(prompter.works, page, per_page, 'prompters.get_prompter_works')
    return jsonify(data)

@prompters.route('/prompters/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    prompter = db.session.query(Prompter).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.followers, page, per_page, 'prompters.get_followers')
    return jsonify(data)

@prompters.route('/prompters/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    prompter = db.session.query(Prompter).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.followed, page, per_page, 'prompters.get_followed')
    return jsonify(data)

@prompters.route('/prompters/<int:id>/followed', methods=['POST'])
@token_auth.login_required
def follow(id):
    pass

@prompters.route('/prompters/<int:follower_id>/followed/<int:followed_id>', methods=['DELETE'])
@token_auth.login_required
def unfollow(follower_id, followed_id):
    pass

@prompters.route('/prompters/<int:id>/liked', methods=['GET'])
@token_auth.login_required
def get_liked(id):
    prompter = db.session.query(Prompter).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.liked, page, per_page, 'prompters.get_liked')
    return jsonify(data)

@prompters.route('/prompters/<int:id>/liked', methods=['POST'])
@token_auth.login_required
def like(id):
    pass

@prompters.route('/prompters/<int:liker_id>/liked/<int:liked_id>', methods=['DELETE'])
@token_auth.login_required
def unlike(liker_id, liked_id):
    pass

@prompters.route('/prompters/<int:id>/feed', methods=['GET'])
@token_auth.login_required
def get_feed(id):
    prompter = db.session.query(Prompter).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Prompter.to_collection.dict(prompter.get_followed_works(), page, per_page, 'prompters.get_feed')
    return jsonify(data)
