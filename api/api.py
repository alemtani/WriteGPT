from app import create_app, db
from app.models import Prompter, Story

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Prompter': Prompter, 'Story': Story}