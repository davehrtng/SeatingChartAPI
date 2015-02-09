from flask import Flask
from flask.ext.restful import Api
from resources.student_api import StudentsByIdApi
from resources.student_api import StudentsApi

app = Flask(__name__)
api = Api(app)


api.add_resource(StudentByIdApi, '/students/<int:id>', endpoint = 'student')
api.add_resource(StudentApi, '/students', endpoint = 'students')