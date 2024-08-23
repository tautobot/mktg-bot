import os
import json
import sys

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Date, DateTime

from database.config import DB_PORT, DB_HOST, DB_NAME, DB_PASS, DB_USER, DB_POOL_SIZE


# build uri
IS_PYTEST       = 'pytest' in sys.modules
XDIST_WORKER    = os.environ.get('PYTEST_XDIST_WORKER')
IS_TEST_SINGLE  = XDIST_WORKER is None or XDIST_WORKER == 'master'
if IS_PYTEST:
    if not IS_TEST_SINGLE:
        DB_NAME    = f'{DB_NAME}_test_x{XDIST_WORKER}'
    else:
        DB_NAME    = f'{DB_NAME}_test'

DB_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# region Create Engine & Scoped Session
def json_dumps_default(val):
    if isinstance(val, DateTime):
        # convert datetime with timezone to string ref. https://stackoverflow.com/a/43414711/248616
        return val.strftime("%Y-%m-%d %H:%M:%S %z")
    elif isinstance(val, Date):
        return val.strftime("%Y-%m-%d")
    else:
        return str(val)


def json_dumps(d):
    return json.dumps(d, default=json_dumps_default)


SCOPED_ENGINE           = create_engine(DB_URI, json_serializer=json_dumps, pool_size=DB_POOL_SIZE)
BACKUP_SCOPED_ENGINE    = create_engine(DB_URI, json_serializer=json_dumps, pool_size=DB_POOL_SIZE)
SESSION_FACTORY = sessionmaker(bind=SCOPED_ENGINE)
SCOPED_SESSION  = scoped_session(SESSION_FACTORY)

# endregion Create Engine & Scoped Session


# region Middleware class
class SQLAlchemySessionManager:
    """
    Create a scoped session for every request and close it when the request ends.
    #                                 =process_resource()           =process_response()
    """

    def __init__(self, Scoped_Session):
        self.Session = Scoped_Session  # Session is Scoped Session

    def process_shutdown(self, scope, event):
        self.Session.remove()

    def process_resource(self, req, resp, resource, params):
        resource.Session = self.Session()  # Session ie PostgresSession

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'Session'):
            try:
                resource.Session.commit()
                if not req_succeeded:
                    resource.Session.rollback()
            except Exception:
                resource.Session.rollback()
            finally:
                if not IS_PYTEST:
                    self.Session.remove()
# endregion Middleware class
