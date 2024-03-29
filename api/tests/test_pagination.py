from datetime import datetime, timedelta
from app import db
from app.models import Prompter, Story
from tests.base_test_case import BaseTestCase

class PaginationTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        prompter = db.session.get(Prompter, 1)
        tm = datetime.utcnow()
        for i in range(105):
            tm -= timedelta(minutes=1)
            story = Story(title=f'Story {i + 1}', prompter=prompter, timestamp=tm)
            db.session.add(story)
        db.session.commit()

    def test_pagination_default(self):
        rv = self.client.get('/api/stories')
        assert rv.status_code == 200
        assert rv.json['_meta']['page'] == 1
        assert rv.json['_meta']['per_page'] == 10
        assert rv.json['_meta']['total_pages'] == 11
        assert rv.json['_meta']['total_items'] == 105
        assert len(rv.json['items']) == 10
        assert rv.json['items'][0]['title'] == 'Story 1'
        assert rv.json['items'][9]['title'] == 'Story 10'
        assert rv.json['_links']['self'] == '/api/stories?page=1&per_page=10'
        assert rv.json['_links']['next'] == '/api/stories?page=2&per_page=10'
        assert rv.json['_links']['prev'] is None

    def test_pagination_page(self):
        rv = self.client.get('/api/stories?page=3')
        assert rv.status_code == 200
        assert rv.json['_meta']['page'] == 3
        assert rv.json['_meta']['per_page'] == 10
        assert rv.json['_meta']['total_pages'] == 11
        assert rv.json['_meta']['total_items'] == 105
        assert len(rv.json['items']) == 10
        assert rv.json['items'][0]['title'] == 'Story 21'
        assert rv.json['items'][9]['title'] == 'Story 30'
        assert rv.json['_links']['self'] == '/api/stories?page=3&per_page=10'
        assert rv.json['_links']['next'] == '/api/stories?page=4&per_page=10'
        assert rv.json['_links']['prev'] == '/api/stories?page=2&per_page=10'

    def test_pagination_last(self):
        rv = self.client.get('/api/stories?page=11')
        assert rv.status_code == 200
        assert rv.json['_meta']['page'] == 11
        assert rv.json['_meta']['per_page'] == 10
        assert rv.json['_meta']['total_pages'] == 11
        assert rv.json['_meta']['total_items'] == 105
        assert len(rv.json['items']) == 5
        assert rv.json['items'][0]['title'] == 'Story 101'
        assert rv.json['items'][4]['title'] == 'Story 105'
        assert rv.json['_links']['self'] == '/api/stories?page=11&per_page=10'
        assert rv.json['_links']['next'] is None
        assert rv.json['_links']['prev'] == '/api/stories?page=10&per_page=10'

    def test_pagination_invalid(self):
        rv = self.client.get('/api/stories?page=0')
        assert rv.status_code == 400
        rv = self.client.get('/api/stories?page=12')
        assert rv.status_code == 400
        rv = self.client.get('/api/stories?per_page=0')
        assert rv.status_code == 400

    def test_pagination_custom_limit(self):
        rv = self.client.get('/api/stories?page=3&per_page=5')
        assert rv.status_code == 200
        assert rv.json['_meta']['page'] == 3
        assert rv.json['_meta']['per_page'] == 5
        assert rv.json['_meta']['total_pages'] == 21
        assert rv.json['_meta']['total_items'] == 105
        assert len(rv.json['items']) == 5
        assert rv.json['items'][0]['title'] == 'Story 11'
        assert rv.json['items'][4]['title'] == 'Story 15'
        assert rv.json['_links']['self'] == '/api/stories?page=3&per_page=5'
        assert rv.json['_links']['next'] == '/api/stories?page=4&per_page=5'
        assert rv.json['_links']['prev'] == '/api/stories?page=2&per_page=5'

    def test_pagination_large_per_page(self):
        rv = self.client.get('/api/stories?per_page=200')
        assert rv.status_code == 200
        assert rv.json['_meta']['page'] == 1
        assert rv.json['_meta']['per_page'] == 100
        assert rv.json['_meta']['total_pages'] == 2
        assert rv.json['_meta']['total_items'] == 105
        assert len(rv.json['items']) == 100
        assert rv.json['items'][0]['title'] == 'Story 1'
        assert rv.json['items'][99]['title'] == 'Story 100'
        assert rv.json['_links']['self'] == '/api/stories?page=1&per_page=100'
        assert rv.json['_links']['next'] == '/api/stories?page=2&per_page=100'
        assert rv.json['_links']['prev'] is None