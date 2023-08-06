from deta import Deta

db_conn = Deta()

def get_db():
    return db_conn