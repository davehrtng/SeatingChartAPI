from flask.ext.restful import Resource, reqparse, fields, marshal
from flask import abort
from data_access import student_collection

# TODO: make ID automatically assigned by mongo when POSTing

student_fields = {
 	'lastName':fields.String,
 	'firstName':fields.String,
 	'uri':fields.Url('student')
 }

# TODO: add error handlers
# for 404, message should identify when the URL was correct but the ID was simply not found
# e.g., when someone requests to GET /students/16 and there is no student with ID 16, then we need to tell the user
# that there URL was formatted fine, we just don't have a student with that ID number

class StudentsApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type = int, required = True, help = 'You must provide an id', location = 'json')
		self.reqparse.add_argument('lastName', type = str, required = True, help = 'lastName field is required', location = 'json')
		self.reqparse.add_argument('firstName', type = str, required = True, help = 'firstName field is required', location = 'json')
		super(StudentsApi, self).__init__()
		
	def get(self):
		return {'students':[marshal(s, student_fields) for s in student_collection.get_all()]}
		
	def post(self):
		args = self.reqparse.parse_args()
		student = {
			'id': args['id'],
			'lastName':args['lastName'],
			'firstName':args['firstName']
		}
		return {'student':marshal(student_collection.insert(student), student_fields)}, 201
	
class StudentsByIdApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('lastName', type=str, required = False, help = 'lastName must be a string', location = 'json')
		self.reqparse.add_argument('firstName', type=str, required = False, help = 'firstName must be a string', location = 'json')
		super(StudentsByIdApi, self).__init__()

	def get(self, id):
		student_list = student_collection.get_by_field_value('id', id)
		if len(student_list) == 0:
			abort(404) # did not find resource with matching id
		return {'student': marshal(student_list[0], student_fields)}
		
	def put(self, id):
		args = self.reqparse.parse_args()
		# create and fill up an update dictionary this way to avoid rather than just pass along whatever they send us to the db
		update_dict = {}
		for key in student_fields:
			if key in args and args[key] is not None:
				update_dict[key] = args[key]
				
		result = student_collection.update({'id':id}, update_dict)
		if result['number_matched'] == 0:
			return {'message':'No resources had the provided id'}, 400
		elif ['number_modified'] == 0:
			return {'message':'Resource already matched your requested changes'}, 200
		else:
			return {}, 204
		
	def delete(self, id):
		"""Remove all students with matching id from the database.
		Returns status 204 if resource was found and deleted. Returns status 404 if the resource was not found."""
		number_deleted = student_collection.delete({'id':id}, True)
		if number_deleted <= 0:
			abort(404)
		else:
			return {}, 204
		