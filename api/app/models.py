import openai
import enum

from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
from datetime import datetime
from app import db

class Genre(enum.Enum):
    default = 0
    fiction = 1
    nonfiction = 2
    poetry = 3
    drama = 4

class Prompter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    works = db.relationship('Work', backref='prompter', lazy='dynamic')

    def __repr__(self):
        return f'<Prompter {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(Enum(Genre))
    title = db.Column(db.String(140))
    body = db.Column(db.String(8000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    prompter_id = db.Column(db.Integer, db.ForeignKey('prompter.id'))

    def __repr__(self):
        return f'<Work {self.title} ({self.genre})>'
    
    def generate_prompt(self):
        if self.genre != Genre.default:
            genre_str = f'{self.genre}'[6:]
            return f"In no more than 8000 characters, write a piece of {genre_str} that responds to the following prompt: '{self.title}'"
        else:
            return f"In no more than 8000 characters, write a creative piece that responds to the following prompt: '{self.title}'"
        
    def generate_completion(self):
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=self.generate_prompt(),
            temperature=0.6,
            max_tokens=2048
        )
        self.body = response.choices[0].text