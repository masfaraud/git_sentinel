import pony.orm
import git_project_management.config as gpmc
import sqlalchemy.exc
import time


def get_sql_db_instance():
    pony_db_instance = pony.orm.Database()
    sql_connect_error = True
    n_connections = 0

    # Connecting to database
    # with app.app_context():
    while sql_connect_error and (n_connections < 20):
        try:
            pony_db_instance.bind(provider=gpmc['SQL_PROVIDER'],
                                  host=gpmc['SQL_HOST'],
                                  user=gpmc['SQL_USER'],
                                  passwd=gpmc['SQL_PASSWORD'],
                                  db=gpmc['SQL_DATABASE'])
            sql_connect_error = False
        except sqlalchemy.exc.OperationalError as err:
            print('Can not connect to SQL DB, retrying in 5 seconds. Error: {}'.format(err))
            n_connections += 1
            time.sleep(5)

    if sql_connect_error:
        raise RuntimeError('Can not connect to administrative SQL database')

    return pony_db_instance


pony_db = get_sql_db_instance()
