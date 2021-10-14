from flask import session

from sql import CrudDatabase


def initialization():
    sql = CrudDatabase()
    query = f"select * from projects order by PID;"

    project_names = sql.fetchRead(query)

    project_names_list = [project.get('PNAME') for project in project_names]

    session["projectNameList"] = project_names_list
    session["allProjects"] = project_names
