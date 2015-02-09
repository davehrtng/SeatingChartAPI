from flask import Flask
from flask.ext.restful import Resource 
from flask.ext.restful import reqparse
from flask.ext.restful import fields, marshal

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
	'uri':fields.Url('task')
}

	
class StudentApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('lastName', type = str, required = True, help = 'No lastName provided', location = 'json')
		self.reqparse.add_argument('firstName', type = str, required = True, help = 'No firstName provided', location = 'json')
		super(StudentApi, self).__init__()

	def get(self, id):
		pass
		
	def put(self, id):
		student = [s for s in students if s['id'] == id]
		if len(student) == 0:
			abort(404)
		student = student[0]
		args = self.reqparse.parse_args()
		for k, v in args.iteritems():
			if v != None:
				student[k] = v
		return {'student': marshal(student, student_fields)}
		
	def delete(self, id):
		pass