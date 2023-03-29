from app import db
from app.models import Prompter
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.exceptions import Unauthorized, Forbidden

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    prompter = db.session.query(Prompter).filter_by(username=username).first()
    if prompter and prompter.check_password(password):
        return prompter
    
@basic_auth.error_handler
def basic_auth_error(status=401):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code, {'WWW-Authenticate': 'Form'}

@token_auth.verify_token
def verify_token(token):
    if current_app.config['DISABLE_AUTH']:
        prompter = db.session.query(Prompter).first()
        prompter.ping()
        return prompter
    return Prompter.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        'code': error.code,
        'message': error.name,
        'description': error.description,
    }, error.code