from flask.ext.restful import Resource, reqparse, fields, marshal
from flask import abort
#from data_access import classes_collection

# TODO: make ID automatically assigned by mongo when POSTing

class_fields = {
 	'name':fields.String,
 	'students':fields.List(fields.Integer),
 	'uri':fields.Url('class')
 }

class ClassesApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('id', type = int, required = True, help = 'You must provide an id', location = 'json')
		self.reqparse.add_argument('name', type = str, required = True, help = 'name field is required', location = 'json')
		self.reqparse.add_argument('students', type = List, required = True, help = 'students field is required', location = 'json')
		super(ClassesApi, self).__init__()
		
	def get(self):
		return {'classes':[marshal(c, class_fields) for c in classes_collection.get_all()]}
		
	def post(self):
		args = self.reqparse.parse_args()
		new_class = {
			'id': args['id'],
			'name':args['name'],
			'students':args['students']
		}
		return {'class':marshal(classes_collection.insert(new_class), class_fields)}, 201
	
class ClassesByIdApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('name', type=str, required = False, help = 'name must be a string', location = 'json')
		self.reqparse.add_argument('students', type=List, required = False, help = 'must provide students: list of integers', location = 'json')
		super(ClassesByIdApi, self).__init__()

	def get(self, id):
		classes_list = classes_collection.get_by_field_value('id', id)
		if len(classes_list) == 0:
			abort(404) # did not find resource with matching id
		return {'student': marshal(classes_list[0], classes_list)}
		
	def put(self, id):
		args = self.reqparse.parse_args()
		# create and fill up an update dictionary this way to avoid rather than just pass along whatever they send us to the db
		update_dict = {}
		for key in classes_fields:
			if key in args and args[key] is not None:
				update_dict[key] = args[key]
				
		result = classes_collection.update({'id':id}, update_dict)
		if result['number_matched'] == 0:
			return {'message':'No resources had the provided id'}, 400
		elif ['number_modified'] == 0:
			return {'message':'Resource already matched your requested changes'}, 200
		else:
			return {}, 204
		
	def delete(self, id):
		"""Remove all students with matching id from the database.
		Returns status 204 if resource was found and deleted. Returns status 404 if the resource was not found."""
		number_deleted = classes_collection.delete({'id':id}, True)
		if number_deleted <= 0:
			abort(404)
		else:
			return {}, 204
		