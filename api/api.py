from app import app, db
from app.models import Genre, Prompter, Work

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Genre': Genre, 'Prompter': Prompter, 'Work': Work}