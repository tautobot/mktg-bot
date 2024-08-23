from uuid import uuid4
from datetime import datetime

from marshmallow import EXCLUDE, fields, Schema, post_load, ValidationError, post_dump

from database.config import TIMEZONE
from database.service.postgres import SCOPED_SESSION

from database.helper.enums import (
    DEFAULT_DATETIME_FORMAT, DEFAULT_DATE_FORMAT,
    UserGenderEnum
)
from database.helper.utils import ParseDataType


"""Custom error message to error code - preapred for translating message error"""
fields.Field.default_error_messages.update({
    'required'          : 'http.fields.required',
    'null'              : 'http.fields.null',
    'validator_failed'  : 'http.validate.failed',
})


class BaseSchema(Schema):

    def __init__(self, *args, **kwargs):
        super(BaseSchema, self).__init__(*args, **kwargs)
        self.Session = SCOPED_SESSION()

    class Meta:
        unknown         = EXCLUDE
        ordered         = True  # keep field-listing-order from model class

    # region fields
    id          = fields.Integer(dump_only=True)
    created_at  = fields.DateTime(dump_only=True, format=DEFAULT_DATETIME_FORMAT)
    updated_at  = fields.DateTime(dump_only=True, format=DEFAULT_DATETIME_FORMAT)
    # endregion fields

    @post_load
    def create(self, data, **kwargs):
        # call model
        model   = self.Meta.model

        # create record
        record  = model.create(**data)
        return record

    @post_dump(pass_many=True)
    def wrap_data(self, data, many, **kwargs):
        if hasattr(self.Meta, 'model'):
            if not many:
                data['object_']     = self.Meta.model.__tablename__
            else:
                for d in data:
                    d['object_']    = self.Meta.model.__tablename__
        return data

    # region handle error
    def handle_error(self, exc, data, **kwargs):
        """
        Override this function to translate error messages
        """
        errors      = exc.messages or exc.messages_dict

        fields      = []
        error_list  = []
        for k, e in errors.items():
            if type(k) == int and type(e) == dict:
                k1          = k + 2
                err_vals    = {str(k1): e}
            else:
                if k != 'column_name':
                    err_vals    = e
                    fields.append(str(k))

            if type(err_vals) == list:
                error_list += err_vals
            else:
                error_list += [err_vals]

        err_dict = {
            'error_code'    : errors.get('error_code') or (error_list and error_list[0] or 'http.general.error'),
            'debug_error'   : errors.get('debug_error') or error_list,
            'fields'        : errors.get('fields') or {'fields': ', '.join(fields)},
            'index'         : self.context.get('index') and str(self.context.get('index')) or None,
            'column_name'   : errors.get('column_name') or errors.get('fields') or f'{fields and fields[0] or None}',
        }

        if err_dict:
            raise ValidationError(message=err_dict, field_name=exc.field_name, data=exc.data)
    # endregion handle error


class DefaultHelper(object):

    def __init__(self, tablename):
        self.table_name = tablename

    def default_today(self):
        dnow = datetime.now(tz=TIMEZONE)
        return dnow.date()


class Lower(fields.Field):
    def __init__(self, inner, *args, **kwargs):
        self.inner = inner
        super().__init__(*args, **kwargs)
        self.validators = self.inner.validators

    def _bind_to_schema(self, field_name, parent):
        super()._bind_to_schema(field_name, parent)
        self.inner._bind_to_schema(field_name, parent)

    def _deserialize(self, value, *args, **kwargs):
        if type(value) == str:
            value = value.strip().replace(' ', '')

        if not value:
            value = None

        if value and hasattr(value, 'lower'):
            value = value.strip().lower()

        return self.inner._deserialize(value, *args, **kwargs)

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)


class Upper(fields.Field):
    def __init__(self, inner, *args, **kwargs):
        self.inner = inner
        super().__init__(*args, **kwargs)
        self.validators = self.inner.validators

    def _bind_to_schema(self, field_name, parent):
        super()._bind_to_schema(field_name, parent)
        self.inner._bind_to_schema(field_name, parent)

    def _deserialize(self, value, *args, **kwargs):
        if type(value) == str:
            value = value.strip()

        if not value:
            value = None
        if value and hasattr(value, 'upper'):
            value = value.upper()
        return self.inner._deserialize(value, *args, **kwargs)

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)


class ConvertString(fields.Integer):

    def _deserialize(self, value, attr, data, **kwargs):
        value = str(value)
        return value


class ConvertUnixTime(fields.Integer):

    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) == int:
            value /= 1000
            value = datetime.fromtimestamp(value).strftime(DEFAULT_DATE_FORMAT)
        return value


class ConvertUnixDateTime(fields.Integer):

    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) == int:
            value /= 1000
            value = datetime.fromtimestamp(value).strftime(DEFAULT_DATETIME_FORMAT)
        return value


class ConvertGender(fields.Str):

    def _deserialize(self, value, attr, data, **kwargs):
        convert_vals = {
            'm'     : UserGenderEnum.MALE,
            'male'  : UserGenderEnum.MALE,
            'f'     : UserGenderEnum.FEMALE,
            'female': UserGenderEnum.FEMALE,
            'o'     : UserGenderEnum.OTHER,
            'other' : UserGenderEnum.OTHER,
        }
        value = convert_vals.get(value.lower())
        return value


class ConvertBool(fields.Str):

    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) == str:
            value = ParseDataType.normalize_boolean(value=value)
        return value


class ConvertObjectId(fields.String):

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Only For loading
        """
        if not value:
            return value
        else:
            mapping_model   = self.metadata.get('mapping_model')
            filter_key      = self.metadata.get('filter_key')
            if not mapping_model or not filter_key:
                raise ValidationError(message={
                    'error_code'    : 'http.general.error',
                    'debug_error'   : ['fields ConvertObjectId missing mapping_model or filter_key'],
                })

            # init Session
            Session = SCOPED_SESSION()

            # convert
            list_value  = [value, value.lower(), value.upper()]
            record      = None
            for lv in list_value:
                filter_vals = {filter_key: lv}
                record      = Session.query(mapping_model).filter_by(**filter_vals).first()
                if record:
                    break
            if not record:
                raise ValidationError(message={
                    'error_code': 'http.record.notfound',
                    'fields'    : {'record_id': f'{value}'},
                })

        return record.id


class ComposeDict(fields.Dict):

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Only For loading
        """
        list_key = self.metadata.get('list_key')
        if not list_key:
            raise ValidationError(message={
                'error_code'    : 'http.general.error',
                'debug_error'   : ['fields ComposeDict missing list_key'],
            })

        # get key and value to compose to dict
        dict_vals = {}
        for lk in list_key:
            # split key
            fkey        = lk.split('::')
            format_key  = fkey[0]
            ftype       = None
            if len(fkey) > 1:
                ftype = fkey[1]

            # convert key
            ckey        = format_key.split('->')
            format_key  = ckey[0]
            converted_k = None
            if len(ckey) > 1:
                converted_k = ckey[1]

            if data.get(format_key):
                fvalue = data.get(format_key)
                if ftype == 'bool':
                    fvalue = ParseDataType.normalize_boolean(fvalue)

                if not converted_k:
                    format_key = format_key.strip().lower().replace(' ', '_')
                else:
                    format_key = converted_k

                dict_vals.update({
                    format_key: fvalue,
                })

        return dict_vals


class ConvertObjectUnitId(ConvertObjectId):

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Only For loading
        """
        if not value:
            return value
        else:
            value = value.replace('ly', 's')

        return super(ConvertObjectUnitId, self)._deserialize(value, attr, data, **kwargs)
