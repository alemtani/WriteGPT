from app import db
from app.auth import token_auth
from app.errors import bad_request
from app.models import Prompter, Work
from flask import abort, Blueprint, jsonify, request, url_for

works = Blueprint('works', __name__)

@works.route('/works', methods=['GET'])
@token_auth.login_required
def get_works():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection_dict(db.session.query(Work), page, per_page, 'works.get_works')
    return jsonify(data)

@works.route('/works', methods=['POST'])
@token_auth.login_required
def create_work():
    prompter = token_auth.current_user()
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title field')
    work = Work(prompter=prompter)
    work.from_dict(data)
    db.session.add(work)
    db.session.commit()
    response = jsonify(work.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('works.get_work', id=work.id)
    return prompter

@works.route('/works/<int:id>', methods=['GET'])
@token_auth.login_required
def get_work(id):
    return jsonify(db.session.query(Work).get_or_404(id).to_dict())

@works.route('/works/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_work(id):
    work = db.session.query(Work).get_or_404(id)
    if work.prompter != token_auth.current_user():
        abort(403)
    data = request.get_json() or {}
    if 'title' in data and data['title'] != work.title and \
            db.session.query(Work).filter_by(title=data['title']).first():
        return bad_request('please use a different title')
    work.from_dict(data)
    db.session.commit()
    return jsonify(work.to_dict())

@works.route('/works/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_work(id):
    work = db.session.query(Work).get_or_404(id)
    if work.prompter != token_auth.current_user():
        abort(403)
    db.session.delete(work)
    db.session.commit()
    return '', 204

@works.route('/works/<int:id>/likers', methods=['GET'])
@token_auth.login_required
def get_likers(id):
    work = db.session.query(Work).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection_dict(work.likers, page, per_page, 'works.get_likers')
    return jsonify(data)