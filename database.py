import pymysql
from pymongo import MongoClient
import certifi

import CONFIG

# print("Database.py")


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
            # print("MongoDB: Exception occured while Connecting to the database.")
            # print(ex)
            return False

    def __disconnect(self):
        try:
            self.client = MongoClient(self.connectionId)
            self.client.close()
            return True
        except Exception as ex:
            print(
                "MongoDB: Exception occured while disconnecting to the database. \nTrying...")
            # print(ex)
            return False

    # def postQuery(self, query):
    # Insert/Post One
    #     query_status = None
    #     collection = self.__connect()
    #     try:
    #         collection.insert_one(query)
    #         query_status = True
    #     except Exception as ex:
    #         query_status = False
    #         # print("MongoDB: Exception occured while Inserting to the database.")
    #         # print(ex)
    #     finally:
    #         self.__disconnect()
    #         return query_status

    # def findOne(self, query):
    # Find one
    #     query_status = None
    #     collection = self.__connect()
    #     try:
    #         result = collection.find_one(query)
    #     except Exception as ex:
    #         query_status = False
    #         # print("MongoDB: Exception occured while performing FindAll in the database.")
    #         # print(ex)
    #     finally:
    #         self.__disconnect()
    #         if query_status == False:
    #             return query_status
    #         return result

    # def updateData(self, query, operation, projection):
    # Update
    #     query_status = None
    #     collection = self.__connect()
    #     try:
    #         collection.update(query, {
    #             operation: projection})
    #         query_status = True
    #     except Exception as ex:
    #         query_status = False
    #         # print("MongoDB: Exception occured while Updating to the database.")
    #         # print(ex)
    #     finally:
    #         self.__disconnect()
    #         return query_status

    # def deleteData(self, projectName):
    # Delete one
    #     query_status = None
    #     collection = self.__connect()
    #     try:
    #         query = {"projectName": projectName}
    #         collection.delete_one(query)
    #         query_status = True
    #     except Exception as ex:
    #         query_status = False
    #         # print("MongoDB: Exception occured while Deleting to the database.")
    #         # print(ex)
    #     finally:
    #         self.__disconnect()
    #         return query_status

    def find(self, query=None, projection=None):
        # Find Many
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find(query, projection)
            return result
        except Exception as ex:
            query_status = False
            # print("MongoDB: Exception occured while performing Find in the database.")
            # print(ex)
            return query_status
        finally:
            self.__disconnect()
            if query_status == False:
                return query_status
            return result


# class SqlDatabase:
#     def __init__(self):
#         self.host = CONFIG.DATABASE[0]
#         self.port = CONFIG.DATABASE[1]
#         self.user = CONFIG.DATABASE[2]
#         self.password = CONFIG.DATABASE[3]
#         self.db = CONFIG.DATABASE[4]

#     def __connect(self):
#         self.con = pymysql.connect(
#             host=self.host,
#             user=self.user,
#             port=self.port,
#             password=self.password,
#             db=self.db,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         self.cur = self.con.cursor()

#     def __commit(self):
#         self.con.commit()

#     def __disconnect(self):
#         self.con.close()

#     def executeWrite(self, sql):
#         #Create, Update, Delete
#         try:
#             self.__connect()
#             self.cur.execute(sql)
#             self.__commit()
#             return True
#         except pymysql.MySQLError as e:
#             # print("Mysql Error:", e)
#             return False
#         finally:
#             self.__disconnect()

#     def fetchRead(self, sql):
#         # Read
#         try:
#             self.__connect()
#             self.cur.execute(sql)
#             result = self.cur.fetchall()
#             if len(result) == 0:
#                 return
#             return result
#         except pymysql.MySQLError as e:
#             # print("Mysql Error:", e)
#             return False
#         finally:
#             self.__disconnect()
