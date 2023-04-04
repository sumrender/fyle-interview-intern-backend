# teacher/assignments tests
def test_get_assignments_teacher_unauthorized(client):
    response = client.get('/teacher/assignments')
    assert response.status_code == 401

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] == 'SUBMITTED'

def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] == 'SUBMITTED'

def test_get_empty_list_assignments(client, h_teacher_3):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_3
    )

    assert response.status_code == 200
    assert len(response.json['data']) == 0

# teacher/assignments/grade tests
def test_grade_assignment_unauthorized(client):
    """
    failure case: should fail since no principal header received
    """
    response = client.get('/teacher/assignments')
    assert response.status_code == 401

def test_grade_assignment_principal_student_error(client, h_student_1):
    """
    failure case: should fail since principal header received is of student
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_student_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    error_response = response.json
    assert response.status_code == 403
    assert error_response['error'] == "FyleError"


def test_grade_assignment_successful(client, h_teacher_1):
    """
    failure case: assignment is not graded by teacher 1
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json['data']

    assert data['grade'] == 'A'
    assert data['state'] == 'GRADED'
    assert data['teacher_id'] == 1

def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment_invalid_payload(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'

def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should not allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'
    
def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
