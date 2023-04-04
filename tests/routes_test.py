def test_ready_route(client):
    response = client.get('/')

    data = response.json
    assert response.status_code == 200
    assert data['status'] == 'ready'

def test_incorrect_route(client):
    response = client.get("/abc/def")

    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'NotFound'

