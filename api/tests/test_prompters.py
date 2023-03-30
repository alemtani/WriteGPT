from tests.base_test_case import BaseTestCase, TestConfigWithAuth

class PrompterTests(BaseTestCase):
    config = TestConfigWithAuth

    def setUp(self):
        super().setUp()
        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        self.token = rv.json['token']

    def test_create_prompter(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'user',
            'email': 'user@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 201
        id = rv.json['id']
        rv = self.client.post('/api/prompters', json={
            'username': 'user',
            'email': 'user2@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 400
        rv = self.client.post('/api/prompters', json={
            'username': 'user2',
            'email': 'user@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 400
        rv = self.client.get(f'/api/prompters/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['username'] == 'user'
        assert rv.json['email'] == 'user@example.com'

    def test_create_invalid_prompter(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'test',
            'email': 'user@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 400
        rv = self.client.post('/api/prompters', json={
            'username': 'user',
            'email': 'test@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 400
        rv = self.client.post('/api/prompters')
        assert rv.status_code == 400

    def test_get_prompters(self):
        rv = self.client.get('/api/prompters', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['username'] == 'test'
        assert rv.json['items'][0]['email'] == 'test@example.com'
        assert 'password' not in rv.json['items'][0]

    def test_get_prompter(self):
        rv = self.client.get('/api/prompters/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['id'] == 1
        assert rv.json['username'] == 'test'
        assert rv.json['email'] == 'test@example.com'
        assert 'password' not in rv.json
        rv = self.client.get('/api/prompters/100', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 404

    def test_edit_prompter_no_changes(self):
        rv = self.client.get('/api/prompters/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        rv2 = self.client.put('/api/prompters/1', json={
            'username': rv.json['username'],
            'email': rv.json['email'],
            'about_me': rv.json['about_me'],
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv2.status_code == 200
        assert rv2.json['username'] == rv.json['username']
        assert rv2.json['email'] == rv.json['email']
        assert rv2.json['about_me'] == rv.json['about_me']

    def test_edit_prompter(self):
        rv = self.client.put('/api/prompters/1', json={
            'about_me': 'I am testing',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['username'] == 'test'
        assert rv.json['email'] == 'test@example.com'
        assert rv.json['about_me'] == 'I am testing'
        assert 'password' not in rv.json

    def test_edit_prompter_invalid(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'user',
            'email': 'user@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.put(f'/api/prompters/{id}', json={
            'about_me': 'I am testing',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

    def test_edit_password(self):
        rv = self.client.put('/api/prompters/1', json={
            'password': 'bar',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 400
        rv = self.client.put('/api/prompters/1', json={
            'old_password': 'foo1',
            'password': 'bar',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 400
        rv = self.client.put('/api/prompters/1', json={
            'old_password': 'foo',
            'password': 'bar',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['username'] == 'test'
        assert rv.json['email'] == 'test@example.com'
        assert 'password' not in rv.json

        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert rv.status_code == 401
        rv = self.client.post('/api/tokens', auth=('test', 'bar'))
        assert rv.status_code == 200
    
    def test_get_prompter_stories(self):
        rv = self.client.post('/api/stories', json={
            'title': 'test'
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201

        rv = self.client.get('/api/prompters/1/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['title'] == 'test'

        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.get(f'/api/prompters/{id}/stories', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

    def test_follow_unfollow(self):
        rv = self.client.get('/api/prompters/1/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get('/api/prompters/1/followers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.get(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert not rv.json['isFollowing']

        rv = self.client.post(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.post(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 409

        rv = self.client.get(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['isFollowing']

        rv = self.client.get('/api/prompters/1/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['username'] == 'susan'

        rv = self.client.get('/api/prompters/1/followers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get(f'/api/prompters/{id}/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get(f'/api/prompters/{id}/followers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['username'] == 'test'

        rv = self.client.delete(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.delete(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 409

        rv = self.client.get(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert not rv.json['isFollowing']

        rv = self.client.get('/api/prompters/1/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get(f'/api/prompters/{id}/followers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []
    
    def test_follow_unfollow_invalid(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.post(f'/api/prompters/{id}/following/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

        rv = self.client.get(f'/api/prompters/{id}/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.delete(f'/api/prompters/{id}/following/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

        rv = self.client.get(f'/api/prompters/{id}/following', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []
    
    def test_like_unlike(self):
        rv = self.client.get('/api/prompters/1/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.post('/api/stories', json={
            'title': 'test'
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.get('/api/prompters/1/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert not rv.json['isLiking']

        rv = self.client.post(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.post(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 409

        rv = self.client.get(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['isLiking']

        rv = self.client.get('/api/prompters/1/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['title'] == 'test'

        rv = self.client.get(f'/api/stories/{id}/likers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['username'] == 'test'

        rv = self.client.delete(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.delete(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 409

        rv = self.client.get(f'/api/prompters/1/liking/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert not rv.json['isLiking']

        rv = self.client.get('/api/prompters/1/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.get(f'/api/stories/{id}/likers', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []
    
    def test_like_unlike_invalid(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.post('/api/stories', json={
            'title': 'test'
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201

        rv = self.client.post(f'/api/prompters/{id}/liking/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

        rv = self.client.get(f'/api/prompters/{id}/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []

        rv = self.client.delete(f'/api/prompters/{id}/liking/1', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

        rv = self.client.get(f'/api/prompters/{id}/liking', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 0
        assert rv.json['items'] == []
    
    def test_get_feed(self):
        rv = self.client.post('/api/prompters', json={
            'username': 'susan',
            'email': 'susan@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        id = rv.json['id']

        rv = self.client.post(f'/api/prompters/1/following/{id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 204

        rv = self.client.post('/api/tokens', auth=('susan', 'dog'))
        self.token = rv.json['token']

        rv = self.client.post('/api/stories', json={
            'title': 'test'
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 201

        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        self.token = rv.json['token']

        rv = self.client.get('/api/prompters/1/feed', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 200
        assert rv.json['_meta']['total_items'] == 1
        assert rv.json['items'][0]['title'] == 'test'

        rv = self.client.get(f'/api/prompters/{id}/feed', headers={
            'Authorization': f'Bearer {self.token}'
        })
        assert rv.status_code == 403

