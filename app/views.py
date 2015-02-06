# i guess the bulk of our routing will go here?
# seems weird

from flask import Flask, jsonify, make_response, request, url_for

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

@app.route('/students', methods=['GET'])
def get_students():
	# return all students
	return jsonify({'students': [make_public_student(student) for student in students]})

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
	#return student with given id
	student = [student for student in students if student['id'] == student_id]
	if len(student) == 0:
		abort(404)
	return jsonify({'student':student[0]})
	
def make_public_student(student):
	new_student = {}
	for field in student:
		if field == 'id':
			new_student['uri'] = url_for('get_student', student_id=student['id'], _external=True)
		else:
			new_student[field] = student[field]
	return new_student
	
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
	