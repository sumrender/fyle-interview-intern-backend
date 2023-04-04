from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignment_resources = Blueprint('teacher_assignment_resources', __name__)

@teacher_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def get_all_assignments_submitted_to_teacher(p):
  """Returns list of assignments submitted to teacher"""
  submitted_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
  submitted_assignments_dump = AssignmentSchema().dump(submitted_assignments, many=True)
  return APIResponse.respond(data=submitted_assignments_dump)

@teacher_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
  """Grades the assignment"""
  grade_assignment_payload =  AssignmentGradeSchema().load(incoming_payload)

  graded_assignment = Assignment.grade_me(
     _id=grade_assignment_payload.id,
     grade_val=grade_assignment_payload.grade,
     principal=p
  )
  db.session.commit()
  graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
  return APIResponse.respond(data=graded_assignment_dump)