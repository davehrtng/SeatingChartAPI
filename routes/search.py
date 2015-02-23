# put search routes for all resources here
# I would rather put the searches with the resources, but the app module imports resources, and I need to import app to add non-resource oriented routes

from flask import make_response, jsonify
from app import app
from data_access import student_collection
import datrie

uri_base = "/students"

def make_student_uri(student_id):
	return uri_base + '/' + str(student_id)
	

def make_public_student(student):
	# TODO: should have a uri field instead of id field
	public_student = {}
	for key, value in student.items():
		if key == 'id':
			public_student['uri'] = make_student_uri(value)
		elif key != '_id':
			public_student[key] = value
	return public_student

@app.route('/students/search/<query>', methods=['GET'])
def student_search(query):
	query_dict = {}
	query_dict['lastName'] = '.*' + query + '.*' # use native python regex syntax
	query_dict['firstName'] = '.*' + query + '.*'
	return make_response(jsonify(
		{
			'students':[make_public_student(s) for s in student_collection.get_by_regex(query_dict, False)]
		}), 200)