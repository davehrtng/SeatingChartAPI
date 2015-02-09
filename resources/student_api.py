from flask.ext.restful import Resource, reqparse, fields, marshal
from flask import abort

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

student_fields = {
	'lastName':fields.String,
	'firstName':fields.String,
	'uri':fields.Url('student')
}

class StudentApi(Resource):
	def __init__(self):
		super(StudentApi, self).__init__()
		
	def get(self):
		pass
		
	def post(self):
		pass
	
class StudentByIdApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('lastName', type=str, required = False, help = 'lastName must be a string', location = 'json')
		self.reqparse.add_argument('firstName', type=str, required = False, help = 'firstName must be a string', location = 'json')
		super(StudentApi, self).__init__()

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
		