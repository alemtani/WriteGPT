import random
import click
from flask import Blueprint
from faker import Faker
from app import db
from app.models import Genre, Prompter, Work

fake = Blueprint('fake', __name__)
faker = Faker()

@fake.cli.command()
@click.argument('num', type=int)
def prompters(num):  # pragma: no cover
    """Create the given number of fake prompters."""
    prompters = []
    for i in range(num):
        prompter = Prompter(username=faker.user_name(), email=faker.email(),
                    about_me=faker.sentence())
        prompter.set_password(faker.password())
        prompter.get_token()
        prompters.append(prompter)

    # create some followers as well
    for prompter in prompters:
        num_followers = random.randint(0, 5)
        for i in range(num_followers):
            following = random.choice(prompters)
            if prompter != following:
                prompter.follow(following)

    db.session.commit()
    print(num, 'prompters added.')

@fake.cli.command()
@click.argument('num', type=int)
def works(num):  # pragma: no cover
    """Create the given number of fake works, assigned to random prompters."""
    prompters = db.session.scalars(db.session.query(Prompter)).all()
    works = []
    for i in range(num):
        prompter = random.choice(prompters)
        work = Work(title=faker.paragraph(nb_sentences=1), prompter=prompter,
                    timestamp=faker.date_time_this_year())
        work.genre = random.choice(list(Genre))
        work.generate_completion()
        db.session.add(work)
        works.append(work)
    
    # create some liked works as well
    for prompter in prompters:
        num_liked = random.randint(0, 10)
        for i in range(num_liked):
            liking = random.choice(works)
            prompter.like(liking)

    db.session.commit()
    print(num, 'works added.')