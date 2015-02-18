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
		return self.get_by_objectId(self.collection.insert(document_dict))
	
	def bulk_insert(self, list_of_dict):
		"""Inserts into collection all documents represented by dictionaries in list_of_dict. Returns list of ObjectIds for inserted documents."""
		return self.collection.insert(list_of_dict)
	
	def get_all(self):
		"""Returns a list of dictionaries representing all documents in collectin"""
		return list(self.collection.find())
	
	def get_by_objectId(self, objectId):
		"""Returns a dictionary of the document with the provided object id"""
		return self.collection.find_one({'_id': bson.ObjectId(objectId)})
		
	def get_matching(self, query_dict):
		"""Returns a list of dictionaries representing all documents with field = value"""
		return list(self.collection.find(query_dict))
		
	def update(self, query_dict, update_dict):
		"""Updates all documents matching query_dict to have values in update_dict. Returns a dictionary with number_matched and number_modified, 
		referring to the number of documents affected by the update."""
		result_dict = self.collection.update(query_dict, {"$set": update_dict}, multi=True, upsert=False)
		return {
			'number_matched':result_dict['n'],
			'number_modified':result_dict['nModified']
		}
	
	def delete(self, query_dict, multi):
		"""Removes document(s) matching the query_dict from the collection. If multi is False, then removes at most 1 document.
		Returns the number of documents deleted."""
		return self.collection.remove(query_dict, multi)['n'];