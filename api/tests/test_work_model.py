from app import db
from app.models import Genre, Prompter, Work
from tests.base_test_case import BaseTestCase

class WorkModelTests(BaseTestCase):
    def test_genre_prompt(self):
        prompter = db.session.get(Prompter, 1)
        w1 = Work(title='test default', prompter=prompter)
        w2 = Work(title='test fiction', genre=Genre.fiction, prompter=prompter)
        w3 = Work(title='test nonfiction', genre=Genre.nonfiction, prompter=prompter)
        w4 = Work(title='test poetry', genre=Genre.poetry, prompter=prompter)
        w5 = Work(title='test drama', genre=Genre.drama, prompter=prompter)
        db.session.add_all([w1, w2, w3, w4, w5])
        db.session.commit()

        self.assertEqual(w1.generate_prompt(), "In no more than 8000 characters, write a creative piece that responds to the following prompt: 'test default'")
        self.assertEqual(w2.generate_prompt(), "In no more than 8000 characters, write a piece of fiction that responds to the following prompt: 'test fiction'")
        self.assertEqual(w3.generate_prompt(), "In no more than 8000 characters, write a piece of nonfiction that responds to the following prompt: 'test nonfiction'")
        self.assertEqual(w4.generate_prompt(), "In no more than 8000 characters, write a piece of poetry that responds to the following prompt: 'test poetry'")
        self.assertEqual(w5.generate_prompt(), "In no more than 8000 characters, write a piece of drama that responds to the following prompt: 'test drama'")