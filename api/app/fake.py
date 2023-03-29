import random
import click
from flask import Blueprint
from faker import Faker
from app import db
from app.models import Prompter, Story

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
def stories(num):  # pragma: no cover
    """Create the given number of fake stories, assigned to random prompters."""
    prompters = db.session.query(Prompter).all()
    stories = []
    for i in range(num):
        prompter = random.choice(prompters)
        story = Story(title=faker.paragraph(nb_sentences=1), prompter=prompter,
                    timestamp=faker.date_time_this_year())
        story.generate_completion()
        db.session.add(story)
        stories.append(story)
    
    # create some liked stories as well
    for prompter in prompters:
        num_liked = random.randint(0, 10)
        for i in range(num_liked):
            liking = random.choice(stories)
            prompter.like(liking)

    db.session.commit()
    print(num, 'stories added.')