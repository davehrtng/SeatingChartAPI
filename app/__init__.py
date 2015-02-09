from flask import Flask
from flask.ext.restful import Api
from resources.student_api import StudentsApi
from resources.student_api import StudentsByIdApi

app = Flask(__name__)
api = Api(app)


api.add_resource(StudentsByIdApi, '/students/<int:id>', endpoint = 'student')
api.add_resource(StudentsApi, '/students', endpoint = 'students')