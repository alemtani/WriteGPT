import base64
import enum
import jwt
import openai
import os

from app import db
from datetime import datetime, timedelta
from flask import current_app, url_for
from hashlib import md5
from sqlalchemy import Enum
from time import time
from werkzeug.security import check_password_hash, generate_password_hash

followers = db.Table('follower',
    db.Column('follower_id', db.Integer, db.ForeignKey('prompter.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('prompter.id'), primary_key=True)
)

likers = db.Table('liker',
    db.Column('liker_id', db.ForeignKey('prompter.id'), primary_key=True),
    db.Column('liked_id', db.ForeignKey('work.id'), primary_key=True)
)

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page+1, per_page=per_page, 
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page-1, per_page=per_page, 
                                **kwargs) if resources.has_prev else None,
            }
        }
        return data

class Genre(enum.Enum):
    default = 0
    fiction = 1
    nonfiction = 2
    poetry = 3
    drama = 4

class Prompter(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    works = db.relationship('Work', backref='prompter', lazy='dynamic')
    followed = db.relationship(
        'Prompter', secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers',lazy='dynamic'), lazy='dynamic')
    liked = db.relationship('Work', secondary=likers, back_populates='likers', lazy='dynamic')

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
        return self.liked.filter(likers.c.liked_id == work.id).count() > 0
    
    def followed_works(self):
        return db.session.query(Work).join(
            followers, (followers.c.followed_id == Work.prompter_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Work.timestamp.desc())
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], 
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(Prompter, id)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            'work_count': self.works.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            'liked_count': self.liked.count(),
            '_links': {
                'self': url_for('prompters.get_prompter', id=self.id),
                'works': url_for('prompters.get_prompter_works', id=self.id),
                'followers': url_for('prompters.get_followers', id=self.id),
                'following': url_for('prompters.get_following', id=self.id),
                'liked': url_for('prompters.get_liked', id=self.id),
                'feed': url_for('prompters.get_feed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        return data
    
    def from_dict(self, data):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])
    
    def ping(self):
        self.last_seen = datetime.utcnow()
    
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    @staticmethod
    def check_token(token):
        prompter = db.session.query(Prompter).filter_by(token=token).first()
        if prompter is None or prompter.token_expiration < datetime.utcnow():
            return None
        prompter.ping()
        return prompter

class Work(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(Enum(Genre), default=Genre.default)
    title = db.Column(db.String(140), index=True, unique=True)
    body = db.Column(db.String(8000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    prompter_id = db.Column(db.Integer, db.ForeignKey('prompter.id'))
    likers = db.relationship(Prompter, secondary=likers, back_populates='liked', lazy='dynamic')

    def __repr__(self):
        return f'<Work {self.title} ({self.genre})>'
    
    def get_genre(self):
        return f'{self.genre}'[6:]
    
    def generate_prompt(self):
        if self.genre != Genre.default:
            return f"In no more than 8000 characters, write a piece of {self.get_genre()} that responds to the following prompt: '{self.title}'"
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
    
    def to_dict(self):
        data = {
            'id': self.id,
            'genre': self.get_genre(),
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp,
            'prompter': self.prompter.to_dict(),
            'likers_count': self.likers.count(),
            '_links': {
                'self': url_for('works.get_work', id=self.id),
                'likers': url_for('works.get_likers', id=self.id)
            }
        }
        return data
    
    def from_dict(self, data):
        if 'title' in data:
            self.title = data['title']
        if 'genre' in data:
            if data['genre'] == 'fiction':
                self.genre = Genre.fiction
            elif data['genre'] == 'nonfiction':
                self.genre = Genre.nonfiction
            elif data['genre'] == 'poetry':
                self.genre = Genre.poetry
            elif data['genre'] == 'drama':
                self.genre = Genre.drama
            else:
                self.genre = Genre.default
        else:
            self.genre = Genre.default
        self.generate_completion()