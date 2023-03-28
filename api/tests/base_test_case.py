import unittest
from app import create_app, db
from app.models import Prompter
from config import Config

class TestConfig(Config):
    SERVER_NAME = 'localhost:5000'
    TESTING = True
    DISABLE_AUTH = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestConfigWithAuth(TestConfig):
    DISABLE_AUTH = False
    REFRESH_TOKEN_IN_BODY = True

class BaseTestCase(unittest.TestCase):
    config = TestConfig

    def setUp(self):
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        prompter = Prompter(username='test', email='test@example.com')
        prompter.set_password('foo')
        db.session.add(prompter)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()