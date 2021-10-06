# to migrate dimention-data from mongodb to mysql database

from database import MongoDatabase, SqlDatabase

mongo_obj = MongoDatabase()
sql_obj = SqlDatabase()


def fetch_tables(query='SHOW TABLES;'):
    result = sql_obj.fetchRead(query)
    tables = []
    for item in result:
        tables.append(item['Tables_in_dimention_db'])
    print(tables)
    return tables


def check_sql_tables():
    tables_required = ['projects', 'dimention']
    tables_in_db = fetch_tables()
    tables_to_create = list(set(tables_required) - set(tables_in_db))
    print(tables_to_create)
    if len(tables_to_create) != len(tables_required):

        if 'projects' in tables_to_create:
            query = "CREATE TABLE PROJECTS(PID INT NOT NULL AUTO_INCREMENT, PNAME VARCHAR(30) NOT NULL UNIQUE, PRIMARY KEY (PID));"
            sql_obj.executeWrite(query)
            print("CREATED PROJECTS TABLE...")

        if 'dimention' in tables_to_create:
            query = '''create table dimention(dimid int not null auto_increment, 
                                              tag varchar(225) not null, 
                                              length float not null, 
                                              width float, 
                                              area_sqm float, 
                                              area_sqft float, 
                                              rate float, 
                                              amount float, 
                                              PID int not null, 
                                              primary key(dimid), 
                                              foreign key(PID) references projects(PID));'''
            sql_obj.executeWrite(query)
            print("CREATED DIMENTION TABLE...")
    return True


def migrate():
    if True:
        for item in mongo_obj.find():
            print(item)
            projectName = item["projectName"]
            add_proj_to_db_query = "insert into projects(PNAME) values('%s');" % (
                str(projectName))
            print(add_proj_to_db_query)
            sql_obj.executeWrite(add_proj_to_db_query)

            fetch_pid_query = "select pid from projects where pname='%s';" % (
                projectName)
            print(fetch_pid_query)

            project_id = sql_obj.fetchRead(fetch_pid_query)[0]["pid"]
            print(projectName, project_id)

            for dim in range(len(item["dims"])):
                curr_dim = item["dims"][dim]
                print("Current Dimention: #", dim)

                curr_dim["length"] = str(
                    curr_dim["length"]).replace("N/A", "0")
                curr_dim["width"] = str(curr_dim["width"]).replace("N/A", "0")
                curr_dim["sqm"] = str(curr_dim["sqm"]).replace("N/A", "0")
                curr_dim["sqft"] = str(curr_dim["sqft"]).replace("N/A", "0")
                curr_dim["rate"] = str(curr_dim["rate"]).replace("N/A", "0")
                curr_dim["amount"] = str(
                    curr_dim["amount"]).replace("N/A", "0")

                query = '''insert into dimention(tag, length, width, area_sqm, area_sqft, rate, amount, pid) 
                                            VALUES('%s', '%f', '%f', '%f', '%f', '%f', '%f', '%i');''' % (str(curr_dim["name"]), float(curr_dim["length"]), float(curr_dim["width"]), float(curr_dim["sqm"]), float(curr_dim["sqft"]), float(curr_dim["rate"]), float(curr_dim["amount"]), project_id)
                sql_obj.executeWrite(query)
                print(curr_dim)
            print("-->###<--")


migrate()
