# put search routes for all resources here
# I would rather put the searches with the resources, but the app module imports resources, and I need to import app to add non-resource oriented routes

from app import app
from data_access import student_collection


@app.route('/students/search/<query>', methods=['GET'])
def student_search_():
	return "hello world"