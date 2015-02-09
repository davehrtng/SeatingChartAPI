from flask import Flask
from flask.ext.restful import Api
from student_api import StudentApi

app = Flask(__name__)
api = Api(app)

api.add_resource(StudentApi, '/student/<int:id>', endpoint = 'student')