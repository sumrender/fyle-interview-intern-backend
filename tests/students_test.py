# GET student/assignments
def test_get_assignments_student_unauthorized(client):
    response = client.get('/student/assignments')
    assert response.status_code == 401

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1

def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

# POST student/assignments
def test_post_assignments_student_unauthorized(client):
    response = client.post(
        '/student/assignments',
        json={
            'content': 'test unauthorized post'
        })
    assert response.status_code == 401

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
    assert data['grade'] is None

def test_post_assignment_student_2(client, h_student_2):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 2
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
    assert data['grade'] is None

# PUT student/assignments
def test_edit_assignment_student_1_successful(client, h_student_1):
    response = client.post(
        '/student/assignments/',
        headers=h_student_1,
        json={
            'id': 2,
            'content': 'assignment updated'
        })
    data = response.json['data']
    assert response.status_code == 200
    assert data['content'] == 'assignment updated'

def test_edit_assignment_error_for_submitted_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/',
        headers=h_student_1,
        json={
            'id': 1,
            'content': 'assignment updated'
        })
    data = response.json
    assert response.status_code == 400
    assert data['error'] == 'FyleError'
    assert data["message"] == 'only assignment in draft state can be edited'

# POST student/assignments/submit
def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2
    assert data['grade'] is None

def test_submit_assignment_failed_for_invalid_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 99,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

def test_submit_assignment_failed_for_invalid_teacher(client, h_student_2):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 7,
            'teacher_id': 999
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'IntegrityError'

def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
