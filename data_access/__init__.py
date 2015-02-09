# initialize MongoCollections here to be available to resources to import
# the idea will be one collection object per resource object
# don't know if that is a good idea or not...

studentMongoCollection = MongoCollection('localhost', 27017, 'SeatingChartApp', 'students')