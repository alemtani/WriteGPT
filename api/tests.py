import os
import unittest

from app import app, db
from app.models import Genre, Prompter, Work
from datetime import datetime, timedelta

os.environ['DATABASE_URL'] = 'sqlite://'

class PrompterModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        p = Prompter(username='susan')
        p.set_password('cat')
        self.assertFalse(p.check_password('dog'))
        self.assertTrue(p.check_password('cat'))

    def test_follow(self):
        p1 = Prompter(username='john')
        p2 = Prompter(username='susan')
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
        p = Prompter(username='susan')
        w = Work(genre=Genre.default, title='test', prompter=p)
        db.session.add(p)
        db.session.add(w)
        db.session.commit()
        self.assertEqual(p.liked, [])
        self.assertEqual(w.likers, [])

        p.like(w)
        db.session.commit()
        self.assertTrue(p.is_liking(w))
        self.assertEqual(len(p.liked), 1)
        self.assertEqual(p.liked[0].title, 'test')
        self.assertEqual(len(w.likers), 1)
        self.assertEqual(w.likers[0].username, 'susan')

        p.unlike(w)
        db.session.commit()
        self.assertFalse(p.is_liking(w))
        self.assertEqual(len(p.liked), 0)
        self.assertEqual(len(w.likers), 0)

    def test_follow_works(self):
        # create four prompters
        p1 = Prompter(username='john')
        p2 = Prompter(username='susan')
        p3 = Prompter(username='mary')
        p4 = Prompter(username='david')
        db.session.add_all([p1, p2, p3, p4])

        # create four pieces
        now = datetime.utcnow()
        w1 = Work(genre=Genre.fiction, title="piece from john", prompter=p1,
                  timestamp=now + timedelta(seconds=1))
        w2 = Work(genre=Genre.nonfiction, title="piece from susan", prompter=p2,
                  timestamp=now + timedelta(seconds=4))
        w3 = Work(genre=Genre.poetry, title="piece from mary", prompter=p3,
                  timestamp=now + timedelta(seconds=3))
        w4 = Work(genre=Genre.drama, title="piece from david", prompter=p4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([w1, w2, w3, w4])
        db.session.commit()

        # setup the followers
        p1.follow(p2)  # john follows susan
        p1.follow(p4)  # john follows david
        p2.follow(p3)  # susan follows mary
        p3.follow(p4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = p1.followed_works().all()
        f2 = p2.followed_works().all()
        f3 = p3.followed_works().all()
        f4 = p4.followed_works().all()
        self.assertEqual(f1, [w2, w4])
        self.assertEqual(f2, [w3])
        self.assertEqual(f3, [w4])
        self.assertEqual(f4, [])

if __name__ == '__main__':
    unittest.main(verbosity=2)