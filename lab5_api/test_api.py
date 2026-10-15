"""Run with: python -m pytest lab5_api/test_api.py -v (from repo root)."""
import pytest
from . import database

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DATABASE', tmp_path / 'test.db')
    from .app import app
    database.create_db_table()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client

SAMPLE = {"name": "John Doe", "email": "john@example.com", "phone": "067765434567", "address": "Main Street", "country": "Lebanon"}

def test_crud(client):
    assert client.get('/api/users').get_json() == []
    created = client.post('/api/users/add', json=SAMPLE)
    assert created.status_code == 201
    user = created.get_json()
    uid = user['user_id']
    assert uid > 0 and user['name'] == 'John Doe'
    assert client.get(f'/api/users/{uid}').get_json() == user
    assert len(client.get('/api/users').get_json()) == 1
    updated = client.put('/api/users/update', json={**SAMPLE, 'name': 'Jane Doe', 'user_id': uid})
    assert updated.status_code == 200
    assert updated.get_json()['name'] == 'Jane Doe'
    assert client.delete(f'/api/users/delete/{uid}').status_code == 200
    assert client.get(f'/api/users/{uid}').status_code == 404
    assert client.get('/api/users').get_json() == []

def test_bad_requests(client):
    assert client.post('/api/users/add', json={}).status_code == 400
    assert client.post('/api/users/add', data='bad', content_type='text/plain').status_code == 400
    assert client.put('/api/users/update', json={**SAMPLE, 'user_id': 999}).status_code == 404
    assert client.put('/api/users/update', json={**SAMPLE, 'user_id': 'one'}).status_code == 400
    assert client.delete('/api/users/delete/999').status_code == 404
    assert client.get('/api/users/999').status_code == 404
