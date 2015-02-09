from flask.ext.restful import Resource, reqparse, fields, marshal

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
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('lastName', type=str, required = False, help = 'lastName must be a string', location = 'json')
		self.reqparse.add_argument('firstName', type=str, required = False, help = 'firstName must be a string', location = 'json')
		super(StudentApi, self).__init__()

	def get(self, id):
		pass
		
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
		pass