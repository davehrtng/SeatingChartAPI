# put search routes for all resources here
# I would rather put the searches with the resources, but the app module imports resources, and I need to import app to add non-resource oriented routes

from flask import make_response, jsonify
from app import app
from data_access import student_collection
import datrie
import string

def clear_trie():
	"""Remove all key-value pairs from trie"""
	for key in student_trie.keys():
		del student_trie[key]

# need to do this periodically. preferabbly after every update to the mongo db, but mongo doesn't support triggers
# so run every x seconds - maybe every minute
# should be able to do that with threading.Timer, but I cannot get that to work for some reason		
def load_trie():
	"""Load all students from database into the trie"""
	clear_trie()
	student_list = student_collection.get_all()
	for s in student_list:
		student_trie[s['lastName'].lower()] = s
	

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

@app.route('/students/search/lastname/<query>', methods=['GET'])
def student_search_lastname(query):
	return make_response(jsonify(
		{
			'students':[make_public_student(s) for s in student_trie.values(query.lower())]
		}), 200);
	
@app.route('/students/search/<query>', methods=['GET'])
def student_search(query):
	query_dict = {}
	query_dict['lastName'] = '.*' + query + '.*' # use native python regex syntax
	query_dict['firstName'] = '.*' + query + '.*'
	return make_response(jsonify(
		{
			'students':[make_public_student(s) for s in student_collection.get_by_regex(query_dict, False)]
		}), 200)
		
#run when file is loaded 
uri_base = "/students"

student_trie = datrie.Trie(string.ascii_lowercase)
load_trie()