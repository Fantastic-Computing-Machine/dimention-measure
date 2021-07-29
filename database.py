# import pymongo
from pymongo import MongoClient

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
            # print(query)
            response = collection.insert_one(query)
            query_status = True
            return query_status

        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while Inserting to the database.")
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
            # print(query_status)
            return result

        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing FindAll in the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def updateData(self, projectName, projection):
        query_status = None
        try:
            collection = self.__connect()
            collection.update_one({"projectName": projectName}, {
                                  "$set": projection})
            query_status = True
        except Exception as ex:
            output, query_status = False
            print("MongoDB: Exception occured while Updating to the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()

    def deleteData(self, projectName):
        query_status = None
        collection = self.__connect()
        try:
            query = {"projectName": projectName}
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

    def find(self, query=None, projection=None):
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find(query, projection)
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

    def projectInitialization(self, projectName, dims=[]):
        post = {
            "projectName": projectName,
            "dims": dims,
        }

        return post

    def dimsCreator(self, dimId, name, length, width,sqm, sqft, rate):
        post = {
            "dimId": dimId,
            "name": name,
            "length": length,
            "width": width,
            "sqm": sqm,
            "sqft": sqft,
            "rate": rate,
        }
        return post


# # Main
# md = MongoDatabase()

# # print(md.connecting())
# # print(md.disconnecting())


# dims = md.findOne({"projectName": "peru"})["dims"]

# dims.append({'dimId': 0, 'name': 'codezero', 'length': 10.0, 'sqm': 10.0,
#              'sqft': 100.0, 'width': 1076.4, 'rate': 1000000.0})


# result = md.updateData("peru", {"dims": dims})


# print(md.findOne({"projectName": "peru"}))
# print(result)

# mdb = MongoDocumentCreator()
