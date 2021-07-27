import pymongo
from pymongo import MongoClient
import json

import CONFIG


class MongoDatabase:
    def __init__(self):
        self.databaseName = CONFIG.MONGO[0]
        self.clusterName = CONFIG.MONGO[1]
        self.connectionId = str(CONFIG.MONGO[2])
        print(self.connectionId)

    def connecting(self):
        try:
            self.client = MongoClient(self.connectionId)
            db = self.client[self.databaseName]
            collection = db[self.clusterName]
            return collection
        except Exception as ex:
            print("MongoDB: Exception occured while Connecting to the database.")
            print(ex)
            return False

    def disconnecting(self):
        try:
            self.client = MongoClient(self.connectionId)
            self.client.close()
            return True
        except Exception as ex:
            print(
                "MongoDB: Exception occured while disconnecting to the database. \nTrying...")
            print(ex)
            return False

    def __connect(self):
        try:
            self.client = MongoClient(self.connectionId)
            db = self.client[self.databaseName]
            collection = db[self.clusterName]
            return collection
        except Exception as ex:
            print("MongoDB: Exception occured while Connecting to the database.")
            print(ex)
            return False

    def __disconnect(self):
        try:
            self.client = MongoClient(self.connectionId)
            self.client.close()
            return True
        except Exception as ex:
            print(
                "MongoDB: Exception occured while disconnecting to the database. \nTrying...")
            print(ex)
            return False

    def postQuery(self, query):
        query_status = None
        collection = self.__connect()
        try:
            print(query)
            response = collection.insert_one(query)
            output = {'query_Status': 'Successfully Inserted',
                      'Document_ID': str(response.inserted_id)}
            query_status = True
            return query_status

        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Inserting to the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def readData(self, userId=None):
        query_status = None
        collection = self.__connect()
        try:
            if userId is None:
                output = collection.find({})
            else:
                output = collection.find({"userId": userId})
            query_status = True
            return output
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Reading to the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def findOne(self, query):
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find_one(query)
            query_status = True
            print(query_status)
            return result

        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing FindAll in the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def updateData(self, userId):
        query_status = None
        try:
            collection = self.__connect()
            collection.update_one({"userId": userId}, {"$set": {}})
        except Exception as ex:
            output, query_status = False
            print("MongoDB: Exception occured while Updating to the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def deleteData(self, userId):
        query_status = None
        collection = self.__connect()
        try:
            query = {"userId": userId}
            collection.delete_one(query)
            query_status = True
            return query_status
        except Exception as ex:
            output, query_status = False
            print("MongoDB: Exception occured while Deleting to the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def find(self,query = None,projection =None):
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find(query,projection)
            query_status = True
            print(result)
            return result

        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing Find in the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

class MongoDocumentCreator:

    def __init__(self):
        pass

    def projectInitialization(self, projectName,dims =[]):
        post = {
            "projectName": projectName,
            "dims": dims,
        }

        return post

    def dimsCreator(self,dimId,name, length, width, rate):
        post = {
            "dimId": dimId,
            "name": name,
            "length": length,
            "width": width,
            "rate": rate,
        }
        return post


# # Main
md = MongoDatabase()

print(md.connecting())
print(md.disconnecting())

print("**************************")
result = md.find()
for i in result:
    print(i["projectName"])
# mdb = MongoDocumentCreator()
# md.postQuery(mdb.projectInitialization(
#       'Hello_world'))

