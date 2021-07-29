from flask import session

import database


def initialization():
    print()
    print("**********HELPER**************")
    projectNameList = []
    print(session)
    if("projectNameList" in session):
        md = database.MongoDatabase()
        result = md.find({}, {"projectName": 2})
        # print(result)
        for i in result:
            # print(i)
            projectNameList.append(i["projectName"])
        session["projectNameList"] = projectNameList
    else:
        print(session)
    print("********************************")
