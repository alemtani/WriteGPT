from datetime import datetime, timedelta
from unittest import mock
from tests.base_test_case import BaseTestCase, TestConfigWithAuth

class AuthTests(BaseTestCase):
    config = TestConfigWithAuth

    def test_no_auth(self):
        rv = self.client.get('/api/prompters')
        assert rv.status_code == 401

    def test_get_token(self):
        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert rv.status_code == 200
        token = rv.json['token']

        rv = self.client.get('/api/prompters', headers={
            'Authorization': f'Bearer {token}'
        })
        assert rv.status_code == 200
        assert rv.json['items'][0]['username'] == 'test'

        rv = self.client.get('/api/prompters', headers={
            'Authorization': f'Bearer {token + "x"}'
        })
        assert rv.status_code == 401

    def test_token_expired(self):
        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert rv.status_code == 200
        token = rv.json['token']

        with mock.patch('app.models.datetime') as dt:
            dt.utcnow.return_value = datetime.utcnow() + timedelta(days=1)
            rv = self.client.get('/api/prompters', headers={
                'Authorization': f'Bearer {token}'
            })
            assert rv.status_code == 401
    
    def test_revoke(self):
        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert rv.status_code == 200
        token = rv.json['token']

        rv = self.client.get('/api/prompters', headers={
            'Authorization': f'Bearer {token}'
        })
        assert rv.status_code == 200

        rv = self.client.delete('/api/tokens', headers={
            'Authorization': f'Bearer {token}'
        })
        assert rv.status_code == 204

        rv = self.client.get('/api/prompters', headers={
            'Authorization': f'Bearer {token}'
        })
        assert rv.status_code == 401

    def test_no_login(self):
        rv = self.client.post('/api/tokens')
        assert rv.status_code == 401

    def test_bad_login(self):
        rv = self.client.post('/api/tokens', auth=('test', 'bar'))
        assert rv.status_code == 401

    def test_reset_password(self):
        with mock.patch('app.tokens.send_email') as send_email:
            rv = self.client.post('/api/tokens/reset', json={
                'email': 'bad@example.com'
            })
            assert rv.status_code == 400
            rv = self.client.post('/api/tokens/reset', json={
                'email': 'test@example.com'
            })
            assert rv.status_code == 204
        send_email.assert_called_once()
        reset_token = send_email.call_args[1]['token']
        reset_url = send_email.call_args[1]['url']
        assert reset_url == 'http://localhost:3000/reset?token=' + reset_token

        rv = self.client.put('/api/tokens/reset', json={
            'token': reset_token + 'x',
            'new_password': 'bar'
        })
        assert rv.status_code == 400

        rv = self.client.put('/api/tokens/reset', json={
            'token': reset_token,
            'new_password': 'bar'
        })
        assert rv.status_code == 204

        rv = self.client.post('/api/tokens', auth=('test', 'foo'))
        assert rv.status_code == 401

        rv = self.client.post('/api/tokens', auth=('test', 'bar'))
        assert rv.status_code == 200