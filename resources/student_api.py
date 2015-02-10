from flask.ext.restful import Resource, reqparse, fields, marshal
from flask import abort
from data_access import student_collection

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

# TODO: make ID automatically assigned by mongo when POSTing

student_fields = {
	'lastName':fields.String,
	'firstName':fields.String,
	'uri':fields.Url('student')
}

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
		student = [s for s in students if s['id'] == id]
		if len(student) == 0:
			abort(404) # did not find resource with matching id
		return {'student': marshal(student[0], student_fields)}
		
	def put(self, id):
		student = [s for s in students if s['id'] == id]
		if len(student) == 0:
			abort(404)
		student = student[0]
		args = self.reqparse.parse_args()
		print(args)
		for k, v in args.items():
			if v != None:
				student[k] = v
		return {'student': marshal(student, student_fields)}
		
	def delete(self, id):
		student = [s for s in students if s['id'] == id]
		if len(student) == 0:
			abort(404) # did not find resource with matching id
		students.remove(student[0])
		return {'isRemoved':True}
		