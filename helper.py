from flask import session

import database


def initialization():
    projectNameList = []
    md = database.MongoDatabase()
    result = md.find({}, {"projectName": 1, "_id": 0})
    print(result)
    for i in result:
        # print(i)
        projectNameList.append(i["projectName"])
    session["projectNameList"] = projectNameList
