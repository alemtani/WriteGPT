import enum
import openai

from app import db
from datetime import datetime
from hashlib import md5
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

followers = db.Table('follower',
    db.Column('follower_id', db.Integer, db.ForeignKey('prompter.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('prompter.id'), primary_key=True)
)

likers = db.Table('liker',
    db.Column('liker_id', db.ForeignKey('prompter.id'), primary_key=True),
    db.Column('liked_id', db.ForeignKey('work.id'), primary_key=True)
)

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
    followed = db.relationship(
        'Prompter', secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers',lazy='dynamic'), lazy='dynamic')
    liked = db.relationship('Work', secondary=likers, back_populates='likers')

    def __repr__(self):
        return f'<Prompter {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, prompter):
        if not self.is_following(prompter):
            self.followed.append(prompter)

    def unfollow(self, prompter):
        if self.is_following(prompter):
            self.followed.remove(prompter)
    
    def is_following(self, prompter):
        return self.followed.filter(followers.c.followed_id == prompter.id).count() > 0
    
    def like(self, work):
        if not self.is_liking(work):
            self.liked.append(work)
    
    def unlike(self, work):
        if self.is_liking(work):
            self.liked.remove(work)
    
    def is_liking(self, work):
        return work in self.liked
    
    def followed_works(self):
        return db.session.query(Work).join(
            followers, (followers.c.followed_id == Work.prompter_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Work.timestamp.desc())
    
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(Enum(Genre))
    title = db.Column(db.String(140))
    body = db.Column(db.String(8000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    prompter_id = db.Column(db.Integer, db.ForeignKey('prompter.id'))
    likers = db.relationship(Prompter, secondary=likers, back_populates='liked')

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