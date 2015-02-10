import pymongo 
import bson

class MongoCollection:
	
	def __init__(self, host, port, database, collection):
		"""Create a MongoClient to connect to mongodb running at host (string) / port (int). Initialize this object to connect to specified database (string) and collection (string)."""
		self.client = pymongo.MongoClient(host, port)
		self.db = getattr(self.client, database)
		self.collection = getattr(self.db, collection)
	
	def insert(self, document_dict):
		"""Inserts a document represented by the parameter into the collection. Returns the inserted document."""
		return get_by_objectId(self.collection.insert(document_dict))
	
	def bulk_insert(self, list_of_dict):
		"""Inserts into collection all documents represented by dictionaries in list_of_dict. Returns list of ObjectIds for inserted documents."""
		return self.collection.insert(list_of_dict)
	
	def get_all(self):
		"""Returns a list of dictionaries representing all documents in collectin"""
		return list(self.collection.find())
	
	def get_by_objectId(self, objectId):
		"""Returns a dictionary of the document with the provided object id"""
		return self.collection.find_one({'_id': bson.ObjectId(objectId)})
		
	def get_by_field_value(self, field, value):
		"""Returns a list of dictionaries representing all documents with field = value"""
		return list(self.collection.find({field:value}))
		
	def update(self, query_dict, update_dict):
		"""Returns an update result dictionary. Both arguments are field-value pairs. All matches to query will have fields in update_dict set equal to the values in that dict."""
		return self.collection.update(query_dict, {"$set": update_dict}, multi=True)
	
	def delete(self, query_dict, multi):
		"""Removes document(s) matching the query_dict from the collection. If multi is False, then removes at most 1 document."""
		self.collection.remove(query_dict, multi);