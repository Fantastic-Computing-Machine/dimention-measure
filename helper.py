from flask import session

import database
def initialization():
    projectNameList = []
    
    if(not "projectNameList" in session):
        md = database.MongoDatabase()
        result = md.find({}, {"projectName": 2})
        # print(result)
        for i in result:
            # print(i)
            projectNameList.append(i["projectName"])
        session["projectNameList"] = projectNameList
        print("session created")
        return True
    else:
        print("session exists")
        return False
