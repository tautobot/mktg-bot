import math
import string
from random import choice, randint
from uuid import uuid4
import pytz

import dateutil

try:
    from sqlalchemy import Table
    from sqlalchemy.sql.selectable import Alias
except ImportError:
    pass

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from marshmallow import ValidationError

from database.config import TIMEZONE
from database.service.postgres import SCOPED_SESSION
from database.helper.enums import DEFAULT_DATE_FORMAT, DEFAULT_DATETIME_FORMAT, ProductConfigUsedEnum


class OrderDetailsUtil(object):
    @classmethod
    def compute(cls, data):
        # compute subtotal with taxs
        subtotal            = data.get('subtotal') or 0
        tax_computed        = data.get('tax_computed') or 0
        discount_computed   = data.get('discount_computed') or 0
        tax                 = data.get('tax') or 0.0
        quantity            = data.get('converted_quantity')
        unit_price          = data.get('unit_price')
        origin_price        = quantity * unit_price

        if tax and not tax_computed:
            tax_computed = (origin_price - discount_computed) * tax

        subtotal_before_tax = subtotal - tax_computed
        # in case subtotal_before_tax < 0
        if subtotal_before_tax < 0:
            subtotal_before_tax = 0

        subtotal_before_discount = subtotal - tax_computed + discount_computed

        return {
            'subtotal_before_tax'       : round(subtotal_before_tax, 2),
            'tax_in_credit'             : round(tax_computed, 2),
            'discount_reduce_in_credit' : round(discount_computed, 2),
            'subtotal_before_discount'  : round(subtotal_before_discount, 2),
        }


class ComputeDatetimeUtil(object):

    @classmethod
    def compute_end_date(cls, start_date, unit_attr, format=True, **kwargs):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, DEFAULT_DATE_FORMAT)

        try:
            if format:
                computed_date = (
                        start_date + relativedelta(**unit_attr) - timedelta(days=1)
                ).strftime(DEFAULT_DATE_FORMAT)
            else:
                computed_date = start_date + relativedelta(**unit_attr) - timedelta(days=1)
        except Exception:
            computed_date = None

        return computed_date

    @classmethod
    def get_next_date(cls, product_rec, end_date: str, start_date: str) -> dict:
        renewal_config  = product_rec.get_config(config_type=ProductConfigUsedEnum.RENEWAL_DAY[0])
        data            = {}
        if renewal_config:
            prepared_days       = int(renewal_config.get('prepared_days', 0))
            paid_days           = int(renewal_config.get('paid_days', 0))

            convert_end_date    = datetime.strptime(end_date, DEFAULT_DATE_FORMAT)

            # compute prepare date
            n_prepare_date   = None
            if prepared_days:
                n_prepare_date  = convert_end_date - timedelta(days=prepared_days)

            # compute paid date
            next_paid_date      = convert_end_date - timedelta(days=paid_days)

            # build data dict
            data.update({
                'next_prepare_date' : n_prepare_date and n_prepare_date.strftime(DEFAULT_DATE_FORMAT) or start_date,
                'next_paid_date'    : next_paid_date.strftime(DEFAULT_DATE_FORMAT),
            })
        return data

    @classmethod
    def compute_age(cls, dob, **kwargs):
        # make sure dob is date/datetime type
        if type(dob) == str:
            dob = datetime.strptime(dob, DEFAULT_DATE_FORMAT)

        checking_date   = kwargs.get('checking_date')

        if not checking_date:
            today = datetime.now(tz=TIMEZONE).date()
        else:
            if type(checking_date) == str:
                today = datetime.strptime(checking_date, DEFAULT_DATE_FORMAT)
            else:
                today = checking_date

        check_birthday  = (today.month, today.day) < (dob.month, dob.day)
        age             = today.year - dob.year - check_birthday
        return age


class ParseDataType(object):

    @classmethod
    def normalize_boolean(cls, value):
        return value.lower() in ['true', 't', 'y', 'yes', '1', 'on']

    @classmethod
    def round_up(cls, number, round_no):
        if round_no == 0:
            number = math.ceil(number)
        else:
            number = round(number, round_no)
        return number

    @classmethod
    def parse_fk(cls, key, value, unique_field, Model, **kwargs):
        # init session
        session = SCOPED_SESSION()

        if value:
            if type(value) == int:
                rec = session.query(Model).get(value)
                if not rec:
                    raise ValidationError(message={
                        'error_code': 'http.record.notfound',
                        'fields'    : {'record_id': f'{Model}({value})'},
                    })
            elif type(value) == str:
                try:
                    value = int(value)
                except:
                    rec   = session.query(Model).filter_by(**{unique_field: value}).first()
                    if rec:
                        value = rec.id
                    else:
                        raise ValidationError(message={
                            'error_code': 'http.record.notfound',
                            'fields'    : {'record_id': f'{Model}({value})'},
                        })
            else:
                raise ValidationError(message={
                    'error_code': 'http.record.notfound',
                    'fields'    : {'record_id': f'{Model}({value})'},
                })
        else:
            raise ValidationError(message={
                'error_code': 'http.record.notfound',
                'fields'    : {'record_id': f'{Model}({value})'},
            })

        return value

    @classmethod
    def remove_field(cls, fields, data):
        for f in fields:
            if f in data:
                del data[f]

        return data


class FilterData(object):

    @classmethod
    def build_apply_filter(cls, model, **kwargs):
        """
        :param model
        :param kwargs:
            {
                'field_1': 'value_1',
                ...
                'field_n': 'value_n',
            }
        :return: filter_spec = [{'field': 'name', 'op': '==', 'value': 'name_1'}]
        """
        filter_spec = []
        if kwargs:
            for f, v in kwargs.items():
                if hasattr(model, f):
                    if getattr(model, f).comparator.type.python_type == str:
                        v = str(v).strip()
                        filter_spec.append({'field': f, 'op': 'ilike', 'value': f'%{v}%',})

                    elif getattr(model, f).comparator.type.python_type in (int, float, date):
                        v = int(v)
                        filter_spec.append({'field': f, 'op': '==', 'value': v})

                    elif getattr(model, f).comparator.type.python_type == datetime:
                        v = datetime.strptime(v, DEFAULT_DATETIME_FORMAT)
                        v = v.strftime(DEFAULT_DATE_FORMAT)
                        filter_spec.append({
                            'and': [
                                {'field': f, 'op': '>=', 'value': f'{v} 00:00:00',},
                                {'field': f, 'op': '<=', 'value': f'{v} 23:59:59', },
                            ]
                        })

                    elif getattr(model, f).comparator.type.python_type == bool:
                        v = ParseDataType.normalize_boolean(v)
                        filter_spec.append({'field': f, 'op': '==', 'value': v})
        return filter_spec

    @classmethod
    def build_auth_filter(cls, req, model, tablename, **kwargs):
        filter_condition = []
        # safe get user_id
        user_id     = DictHelper.safeget(req.context, 'auth', 'user', 'user_id')
        user_id     = DictHelper.force_int(user_id)
        list_users  = DictHelper.safeget(req.context, 'role_filter', 'user_ids')

        # auto filter based on user_id if table has this key
        if user_id:
            if tablename == 'users':
                # if user model, then filter by user_id
                filter_condition.append({'field': 'id', 'op': '==', 'value': user_id})
            elif hasattr(model, 'user_id'):
                # if not user model, filter by user_id if model has user_id field
                if list_users:
                    filter_condition.append({'field': 'user_id', 'op': 'in', 'value': list_users})
                elif not user_id:
                    filter_condition.append({'field': 'user_id', 'op': 'in', 'value': [-1, -1]})
        else:
            if tablename == 'users':
                # if user model, then filter by user_id
                filter_condition.append({'field': 'id', 'op': '==', 'value': -1})

        return filter_condition


class DictHelper:

    @classmethod
    def safeget(cls, dct: dict, *keys):
        for key in keys:
            try:
                dct = dct[key]
            except Exception:
                return None
        return dct

    @classmethod
    def force_int(cls, value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    @classmethod
    def force_float(cls, value, default=0.0):
        try:
            return float(value)
        except:
            return default

    @classmethod
    def force_str(cls, value, default=''):
        try:
            return str(value)
        except Exception:
            return default


class CountryHelper(object):
    IDN = 'IDN'
    SGP = 'SGP'
    PHL = 'PHL'

    @staticmethod
    def get_nation_mobile(country):
        nation_mapping = {
            CountryHelper.SGP: '65',
            CountryHelper.IDN: '62',
            CountryHelper.PHL: '63',
        }
        return nation_mapping[country]

    @staticmethod
    def format_mobile(mobile, country=None):
        if mobile:
            mob = mobile.strip()
            country = country.upper() if country else CountryHelper.SGP
            nation = CountryHelper.get_nation_mobile(country)
            full_prefix = f'+{nation}'
            if mob.startswith(nation):
                return "+" + mob
            elif mob.startswith(full_prefix):
                return mob
            elif mob.startswith('+'):
                return mobile
            elif mob.startswith('0'):
                return mob[:0] + full_prefix + mob[1:]
            else:
                return full_prefix + mob
        else:
            return mobile


def normalize_to_bool(input):
    if isinstance(input, bool):
        return input

    elif isinstance(input, str):

        if input.lower().strip() == 'true': return True
        if input.lower().strip() == 't':    return True
        if input.lower().strip() == 'True': return True
        if input.lower().strip() == 'T':    return True
        if input.lower().strip() == 'yes':  return True
        if input.lower().strip() == 'Yes':  return True
        if input.lower().strip() == 'y':    return True
        return False

    else:
        return False


def pop_data_assertion(data, fields=[]):

    for f in fields:
        data.pop(f)
    return data


def format_date(date : datetime, country_code=CountryHelper.SGP):
    if not date:
        return ''
    if country_code.upper() == CountryHelper.PHL:
        return date.strftime("%m/%d/%Y")
    else:
        return date.strftime("%d/%m/%Y")


def trim_string_data(string_data):
    if string_data is not None:
        return str(string_data).strip().replace(' ', '') if string_data else ''
    else:
        return string_data


def random_string(length=None):
    allchars = string.ascii_letters + string.digits
    if length:
        return "".join(choice(allchars) for x in range(length))
    else:
        return "".join(choice(allchars) for x in range(randint(8, 24)))


def generate_task_id(prefix=''):
    task_id = f"{prefix}.{uuid4().hex[:10]}.{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
    return task_id


def to_upper(v:'value'):
    if type(v)==str: v = v.upper()
    return v


def to_lower(v:'value'):
    if type(v)==str: v = v.lower()
    return v


def s2d(val: 'str') -> date:  # a shorter version for Utils.normalize_to_date(obj)
    dt = s2dt(val)
    d  = dt.date() if dt else None
    return d


def to_UTC(dt):
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return pytz.utc.localize(dt).astimezone(pytz.timezone('UTC'))
    else:
        return dt.astimezone(pytz.timezone('UTC'))


def s2dt(val:'str') -> datetime:
    """
    handles all conversions of string (with or without timezone) to datetime (with timezone) except YYYY-MM
    if no timezone is stated, UTC is assumed
    """
    if not val: return None

    val = val.strip("'").strip('"')
    try:
        dt = dateutil.parser.parse(val)
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = to_UTC(dt)
        return dt
    except ValueError:
        return None


def format_mobile(mobile, country=CountryHelper.SGP):
    if mobile:
        mob = mobile.strip()
        nation = CountryHelper.get_nation_mobile(country)
        full_prefix = f'+{nation}'
        if mob.startswith(nation):
            return "+" + mob
        elif mob.startswith(full_prefix):
            return mob
        elif mob.startswith('+'):
            return mobile
        elif mob.startswith('0'):
            return mob[:0] + full_prefix + mob[1:]
        else:
            return full_prefix + mob
    else:
        return mobile


def convert2serialize(obj):
    if isinstance(obj, dict):
        return {k: convert2serialize(v) for k, v in obj.items()}
    elif hasattr(obj, "_ast"):
        return convert2serialize(obj._ast())
    elif not isinstance(obj, str) and hasattr(obj, "__iter__"):
        return [convert2serialize(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return {
            k: convert2serialize(v)
            for k, v in obj.__dict__.items()
            if not callable(v) and not k.startswith('_')
        }
    else:
        return obj


def format_short_gender(gender):
    if gender:
        return gender[0].upper()
    return gender


class Dict2Obj:
    def __init__(self, **entries):
        self.__dict__.update(entries)
