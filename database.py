# import pymongo
from pymongo import MongoClient
import certifi

import CONFIG


class MongoDatabase:
    def __init__(self):
        self.databaseName = CONFIG.MONGO[0]
        self.clusterName = CONFIG.MONGO[1]
        self.connectionId = str(CONFIG.MONGO[2])

    def __connect(self):
        try:
            self.client = MongoClient(
                self.connectionId, tlsCAFile=certifi.where())
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
        # Insert/Post One
        query_status = None
        collection = self.__connect()
        try:
            collection.insert_one(query)
            query_status = True
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Inserting to the database.")
            print(ex)
        finally:
            self.__disconnect()
            return query_status

    def findOne(self, query):
        # Find one
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find_one(query)
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing FindAll in the database.")
            print(ex)
        finally:
            self.__disconnect()
            if query_status == False:
                return query_status
            return result

    def updateData(self, query, operation, projection):
        # Update
        query_status = None
        collection = self.__connect()
        try:
            collection.update(query, {
                operation: projection})
            query_status = True
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Updating to the database.")
            print(ex)
        finally:
            self.__disconnect()
            return query_status

    def deleteData(self, projectName):
        # Delete one
        query_status = None
        collection = self.__connect()
        try:
            query = {"projectName": projectName}
            collection.delete_one(query)
            query_status = True
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Deleting to the database.")
            print(ex)
        finally:
            self.__disconnect()
            return query_status

    def find(self, query=None, projection=None):
        # Find Many
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find(query, projection)
            return result
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing Find in the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()
            if query_status == False:
                return query_status
            return result


class MongoDocumentCreator:

    def __init__(self):
        pass

    def projectInitialization(self, projectName, dims=[]):
        post = {
            "projectName": projectName,
            "dims": dims,
        }
        return post

    def dimsCreator(self, dimId, name, length, width, sqm, sqft, rate, amount):
        post = {
            "dimId": dimId,
            "name": name,
            "length": length,
            "width": width,
            "sqm": sqm,
            "sqft": sqft,
            "rate": rate,
            "amount": amount
        }
        return post
