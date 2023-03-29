from tests.base_test_case import BaseTestCase, TestConfigWithAuth

class StoryTests(BaseTestCase):
    config = TestConfigWithAuth

    def setUp(self):
        super().setUp()
        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        self.token = rv.json['token']

    def test_new_story(self):
        rv = self.client.post('/api/stories', json={
            'title': 'This is a test story',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        assert rv.json['title'] == 'This is a test story'
        assert rv.json['prompter']['username'] == 'test'
        id = rv.json['id']

        rv = self.client.get(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['title'] == 'This is a test story'

        rv = self.client.get('/api/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['title'] == 'This is a test story'

        rv = self.client.get('/api/prompters/1/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['title'] == 'This is a test story'

        rv = self.client.get('/api/prompters/2/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 404
    
    def test_new_story_invalid(self):
        rv = self.client.post('/api/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 400

    def test_edit_story(self):
        rv = self.client.post('/api/stories', json={
            'title': 'This is a test story',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        assert rv.json['title'] == 'This is a test story'
        id = rv.json['id']

        rv = self.client.put(f'/api/stories/{id}', json={
            'title': 'This is a test story edited',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['title'] == 'This is a test story edited'

        rv = self.client.get(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['title'] == 'This is a test story edited'
    
    def test_edit_story_invalid(self):
        rv = self.client.post('/api/stories', json={
            'title': 'This is a test story',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        assert rv.json['title'] == 'This is a test story'
        id = rv.json['id']

        rv = self.client.put(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 400

        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201

        rv = self.client.post('/api/tokens', auth=('susan', 'dog'))
        self.token = rv.json['token']

        rv = self.client.put(f'/api/stories/{id}', json={
            'title': 'This is a test story edited',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

    def test_delete_story(self):
        rv = self.client.post('/api/stories', json={
            'title': 'This is a test story',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        assert rv.json['title'] == 'This is a test story'
        id = rv.json['id']

        rv = self.client.delete(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.get(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 404
    
    def test_delete_story_invalid(self):
        rv = self.client.post('/api/stories', json={
            'title': 'This is a test story',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        assert rv.json['title'] == 'This is a test story'
        id = rv.json['id']

        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201

        rv = self.client.post('/api/tokens', auth=('susan', 'dog'))
        self.token = rv.json['token']

        rv = self.client.delete(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

        rv = self.client.get(f'/api/stories/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200