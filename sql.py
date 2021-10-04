import pymysql
import CONFIG


class CrudDatabase:
    def __init__(self):
        self.host = CONFIG.DATABASE[0]
        self.port = CONFIG.DATABASE[1]
        self.user = CONFIG.DATABASE[2]
        self.password = CONFIG.DATABASE[3]
        self.db = CONFIG.DATABASE[4]

    def __connect(self):
        self.con = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            db=self.db,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def __commit(self):
        self.con.commit()

    def __disconnect(self):
        self.con.close()

    def executeWrite(self, sql):
        #Create, Update, Delete
        try:
            self.__connect()
            # if isinstance(sql, list):
            #     for query in sql:
            #         self.cur.execute(query)
            # if isinstance(sql, str):
            #     self.cur.execute(sql)
            self.cur.execute(sql)
            self.__commit()
            return True
        except pymysql.MySQLError as e:
            print("Mysql Error:", e)
            return False
        finally:
            self.__disconnect()

    # def executeWrite(self, sql):
    #     # Multiple Create, Update, Delete
    #     try:
    #         self.__connect()
    #         self.cur.execute(sql)
    #         self.__commit()
    #         return True
    #     except pymysql.MySQLError as e:
    #         print("Mysql Error:", e)
    #         return False
    #     finally:
    #         self.__disconnect()

    def fetchRead(self, sql):
        # Read
        try:
            self.__connect()
            self.cur.execute(sql)
            result = self.cur.fetchall()
            if len(result) == 0:
                return
            return result
        except pymysql.MySQLError as e:
            print("Mysql Error:", e)
            return False
        finally:
            self.__disconnect()
