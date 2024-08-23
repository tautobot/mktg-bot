from marshmallow import fields
from marshmallow.validate import Length

from database.mm_schema._base import BaseSchema, DefaultHelper
from database.model.multimedia import Multimedia
from marshmallow import fields, pre_load, post_dump, post_load, EXCLUDE

default_helper = DefaultHelper(tablename=Multimedia.__tablename__)


class MULTIMEDIA_SCHEMA(BaseSchema):

    def __init__(self, *args, **kwargs):
        super(MULTIMEDIA_SCHEMA, self).__init__(*args, **kwargs)

    class Meta:
        model   = Multimedia

    external_id      = fields.Str(allow_none=True)
    title            = fields.Str(allow_none=True)
    tags             = fields.Str(allow_none=True)
    lyric            = fields.Str(allow_none=True)
    image_url        = fields.Str(allow_none=True)
    audio_url        = fields.Str(allow_none=True)
    video_url        = fields.Str(allow_none=True)
    duration         = fields.Float(allow_none=True)
    source           = fields.Str(allow_none=True)
    model_name       = fields.Str(allow_none=True)
    model_version    = fields.Str(allow_none=True)

    # country_obj      = fields.Method('_get_country_obj')
    # Age              = fields.Method('_get_age')

    # def _get_country_obj(self, obj):
    #     from phoenix.model import Country
    #     from phoenix.mm_schema.countries_schema import COUNTRIES_SCHEMA
    #
    #     country_rec     = self.Session.query(Country).get(obj.country_id)
    #     country_json    = COUNTRIES_SCHEMA().dump(country_rec)
    #     return country_json

    # def _get_age(self, obj):
    #     age = None
    #     if obj.dob:
    #         age = ComputeDatetimeUtil.compute_age(dob=obj.dob)
    #     return age
