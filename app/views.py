# i guess the bulk of our routing will go here?
# seems weird

from flask import Flask, jsonify, make_response, request, url_for, abort

from app import app

students = [
	{
		'id':1,
		'lastName':'Harting',
		'firstName':'David'
	},
	{
		'id':2,
		'lastName':'Phillips',
		'firstName':'Reggie'
	},
	{
		'id':3,
		'lastName':'Palmer',
		'firstName':'Arnold'
	}
]

# read all students
@app.route('/students', methods=['GET'])
def get_students():
	# return all students
	return jsonify({'students': [make_public_student(student) for student in students]})

# read student by id
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
	#return student with given id
	student = [student for student in students if student['id'] == student_id]
	if len(student) == 0:
		abort(404)
	return jsonify({'student':student[0]})

# create student
@app.route('/students', methods=['POST'])
def create_student():
	#persist a new student
	if not request.json or 'lastName' not in request.json or 'firstName' not in request.json:
		abort(400)
	new_student = {
		'id':next_student_id(),
		'lastName':request.json['lastName'],
		'firstName':request.json['firstName']
	}
	students.append(new_student)
	return make_response(jsonify({'student':new_student}), 201)
	
# delete student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
	student = [student for student in students if student['id'] == student_id]
	if len(student) == 0: #no student with provided id
		abort(404)
	students.remove(student[0])
	return jsonify({'result':True})
	
def make_public_student(student):
	new_student = {}
	for field in student:
		if field == 'id':
			new_student['uri'] = url_for('get_student', student_id=student['id'], _external=True)
		else:
			new_student[field] = student[field]
	return new_student

def next_student_id():
	"""Lookup the next available student id"""
	return max(map(lambda s: s['id'], students)) + 1

@app.errorhandler(400)
#TODO: specify what went wrong
def bad_request(error):
	return make_response(jsonify({
		'error':'Bad request',
		'errorCode':400,
		'displayableText':'The application asked for data incorrectly'
		}), 400)
	
@app.errorhandler(404)
# TODO: differentiate between bad URL and bad ID
def not_found(error):
	return make_response(jsonify({
		'error': 'Not found',
		'errorCode':404,
		'displayableText':'The requested content could not be found'
		}), 404)
		
	