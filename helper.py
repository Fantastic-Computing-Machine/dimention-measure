from flask import session

from sql import CrudDatabase


def initialization():
    project_names_list = []
    sql = CrudDatabase()
    query = "select * from projects order by PID;"

    project_names = sql.fetchRead(query)

    for project in project_names:
        project_names_list.append(project.get('PNAME'))
    # print(project_names_list)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(project_names)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@")

    session["projectNameList"] = project_names_list
    session["allProjects"] = project_names
