from app import db
from app.auth import basic_auth
from flask import Blueprint, jsonify

tokens = Blueprint('tokens', __name__)

@tokens.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

def revoke_token():
    pass