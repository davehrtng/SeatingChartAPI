# initialize MongoCollections here to be available to resources to import
# the idea will be one collection object per resource object

from data_access.db_connector import MongoCollection 

student_collection = MongoCollection('localhost', 27017, 'SeatingChartApp', 'students')