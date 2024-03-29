from app import db
from app.models import Prompter, Story
from datetime import datetime, timedelta
from tests.base_test_case import BaseTestCase

class PrompterModelTests(BaseTestCase):
    def test_password_hashing(self):
        p = Prompter(username='susan')
        p.set_password('cat')
        self.assertFalse(p.check_password('dog'))
        self.assertTrue(p.check_password('cat'))
    
    def test_avatar(self):
        p = Prompter(username='john', email='john@example.com')
        self.assertEqual(p.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        p1 = Prompter(username='john', email='john@example.com')
        p2 = Prompter(username='susan', email='susan@example.com')
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        self.assertEqual(p1.followed.all(), [])
        self.assertEqual(p1.followers.all(), [])

        p1.follow(p2)
        db.session.commit()
        self.assertTrue(p1.is_following(p2))
        self.assertEqual(p1.followed.count(), 1)
        self.assertEqual(p1.followed.first().username, 'susan')
        self.assertEqual(p2.followers.count(), 1)
        self.assertEqual(p2.followers.first().username, 'john')

        p1.unfollow(p2)
        db.session.commit()
        self.assertFalse(p1.is_following(p2))
        self.assertEqual(p1.followed.count(), 0)
        self.assertEqual(p2.followers.count(), 0)
    
    def test_like(self):
        p = Prompter(username='susan', email='susan@example.com')
        s = Story(title='test', prompter=p)
        db.session.add(p)
        db.session.add(s)
        db.session.commit()
        self.assertEqual(p.liked.all(), [])
        self.assertEqual(s.likers.all(), [])

        p.like(s)
        db.session.commit()
        self.assertTrue(p.is_liking(s))
        self.assertEqual(p.liked.count(), 1)
        self.assertEqual(p.liked.first().title, 'test')
        self.assertEqual(s.likers.count(), 1)
        self.assertEqual(s.likers.first().username, 'susan')

        p.unlike(s)
        db.session.commit()
        self.assertFalse(p.is_liking(s))
        self.assertEqual(p.liked.count(), 0)
        self.assertEqual(s.likers.count(), 0)

    def test_follow_stories(self):
        # create four prompters
        p1 = Prompter(username='john', email='john@example.com')
        p2 = Prompter(username='susan', email='susan@example.com')
        p3 = Prompter(username='mary', email='mary@example.com')
        p4 = Prompter(username='david', email='david@example.com')
        db.session.add_all([p1, p2, p3, p4])

        # create four pieces
        now = datetime.utcnow()
        s1 = Story(title="piece from john", prompter=p1, timestamp=now + timedelta(seconds=1))
        s2 = Story(title="piece from susan", prompter=p2, timestamp=now + timedelta(seconds=4))
        s3 = Story(title="piece from mary", prompter=p3, timestamp=now + timedelta(seconds=3))
        s4 = Story(title="piece from david", prompter=p4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        # setup the followers
        p1.follow(p2)  # john follows susan
        p1.follow(p4)  # john follows david
        p2.follow(p3)  # susan follows mary
        p3.follow(p4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = p1.followed_stories().all()
        f2 = p2.followed_stories().all()
        f3 = p3.followed_stories().all()
        f4 = p4.followed_stories().all()
        self.assertEqual(f1, [s2, s4])
        self.assertEqual(f2, [s3])
        self.assertEqual(f3, [s4])
        self.assertEqual(f4, [])