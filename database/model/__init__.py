from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import MetaData, Column, Integer, func, DateTime
from sqlalchemy.ext.declarative import declarative_base

from marshmallow import ValidationError

from database.service.postgres import SCOPED_SESSION
# import phoenix.service.celery_worker.worker as CeleryApp
from database.helper.utils import ParseDataType
from database.helper.enums import DEFAULT_DATETIME_FORMAT


class BaseModel(object):

    # region sqlalchemy column
    id          = Column(Integer, primary_key=True)
    created_at  = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    updated_at  = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True
    )
    # endregion sqlalchemy column

    def m2s(self, featured=None):  # m2s aka. model to string
        if featured is None:
            featured = ['id']
        fa = {f: getattr(self, f) for f in featured if hasattr(self, f)}  # fa aka. featured attributes
        cn = self.__class__.__name__  # cn aka. class name
        return f'{cn}({fa})'

    def __str__(self):  return self.m2s()

    def __repr__(self): return self.m2s()

    def to_dict(self):
        d = {}
        columns = self._sa_class_manager.mapper.mapped_table.columns
        for c in columns:
            d[c.name] = getattr(self, c.name)
        from sqlalchemy.inspection import inspect as sa_inspect
        from sqlalchemy.ext.hybrid import hybrid_property
        for item in sa_inspect(self.__class__).all_orm_descriptors:
            if type(item) == hybrid_property:
                # ha means hybrid-property attribute aka. hybrid attribute
                ha = item.__name__
                d[ha] = getattr(self, ha)
        return d

    # region orm helper
    @classmethod
    def create(cls, **kwargs):
        # get session
        Session = SCOPED_SESSION()

        # create record
        record  = cls(**kwargs)

        # store into db
        Session.add(record)
        Session.commit()

        return record

    @classmethod
    def parse_value(cls, key, value):
        if hasattr(cls, key):
            v = value
            f = getattr(cls, key)
            if f.comparator.type == Integer:
                v = int(value)
            elif f.comparator.type == sa.String:
                v = str(value)
            elif f.comparator.type == sa.Boolean:
                v = ParseDataType().normalize_boolean(value)

            return v

        else:
            return None

    def write(self, **kwargs):
        # import phoenix.service.celery_worker.celery_task as ctask
        try:
            # get session
            Session = SCOPED_SESSION()

            for k, v in kwargs.items():
                if hasattr(self, k):
                    old_value = getattr(self, k)
                    if str(type(old_value)) != "<class 'method'>":
                        setattr(self, k, v)

                        # store changing data on column
                        db_log_body = {
                            'table_name'        : self.__tablename__,
                            'primary_key_value' : self.id,
                            'column_name'       : k,
                            'old_value'         : str(old_value),
                            'new_value'         : str(v),
                            'created_at'        : datetime.utcnow().strftime(DEFAULT_DATETIME_FORMAT),
                            'user_id'           : None,
                        }
                        task_id = f"mktg.add_change_log_database." \
                                  f"{uuid4().hex[:10]}.{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
                        # CeleryApp.delay(ctask.add_change_log_database, task_id, db_log_body)(task_id=task_id)

            Session.commit()
        except Exception as e:
            raise ValidationError(message={
                'error_code'    : 'http.general.error',
                'debug_error'   : f'{e}',
            })

    def delete(self, **kwargs):
        # get session
        Session = SCOPED_SESSION()

        Session.delete(self)

        Session.commit()

    # endregion orm helper


meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
MktgBaseModel = declarative_base(cls=BaseModel, metadata=meta)


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in MktgBaseModel.registry.mappers:
        if c.mapped_table.name == tablename:
            return c.class_
    return None


# init model here
from database.model.multimedia import Multimedia
