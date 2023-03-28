from app import db
from app.auth import token_auth
from app.errors import bad_request
from app.models import Prompter, Work
from flask import Blueprint, jsonify, request, url_for

works = Blueprint('works', __name__)

@works.route('/works', methods=['GET'])
@token_auth.login_required
def get_works():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection.dict(db.session.query(Work), page, per_page, 'works.get_works')
    return jsonify(data)

@works.route('/works', methods=['POST'])
@token_auth.login_required
def create_work():
    prompter = token_auth.current_user()
    data = request.get_json() or {}
    # TODO

@works.route('/works/<int:id>', methods=['GET'])
@token_auth.login_required
def get_work(id):
    return jsonify(db.session.query(Work).get_or_404(id).to_dict())

@works.route('/works/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_work(id):
    pass

@works.route('/works/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_work(id):
    pass

@works.route('/works/<int:id>/likers', methods=['GET'])
@token_auth.login_required
def get_likers(id):
    work = db.session.query(Work).get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Work.to_collection.dict(work.likers, page, per_page, 'works.get_likers')
    return jsonify(data)