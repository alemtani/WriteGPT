from app import db
from app.auth import basic_auth, token_auth
from app.email import send_email
from app.errors import bad_request
from app.models import Prompter
from flask import abort, Blueprint, current_app, jsonify, request

tokens = Blueprint('tokens', __name__)

@tokens.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@tokens.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204

@tokens.route('/tokens/reset', methods=['POST'])
def reset():
    data = request.get_json() or {}
    if 'email' not in data:
        return bad_request('must include email field')
    prompter = db.session.query(Prompter).filter_by(email=data['email']).first()
    if not prompter:
        abort(404)
    reset_token = prompter.get_reset_password_token()
    reset_url = f"{current_app.config['BASE_CLIENT_URL']}/reset?token={reset_token}"
    send_email('[WriteGPT] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[prompter.email],
               template='reset_password',
               token=reset_token,
               url=reset_url)
    return {}, 204

@tokens.route('/tokens/reset', methods=['PUT'])
def password_reset():
    data = request.get_json() or {}
    if 'token' not in data or 'new_password' not in data:
        return bad_request('must include token and new_password fields')
    prompter = Prompter.verify_reset_password_token(data['token'])
    if not prompter:
        abort(404)
    prompter.set_password(data['new_password'])
    db.session.commit()
    return {}, 204
