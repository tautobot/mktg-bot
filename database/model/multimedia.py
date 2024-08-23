import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from database.model import MktgBaseModel
from database.service.postgres import SCOPED_SESSION
from marshmallow import fields, pre_load, post_dump, post_load, EXCLUDE


class Multimedia(MktgBaseModel):
    __tablename__ = 'multimedia'

    external_id   = sa.Column('external_id', sa.String(), nullable=True)
    title         = sa.Column('title', sa.String(), nullable=True)
    tags          = sa.Column('tags', sa.String(), nullable=True)
    lyric         = sa.Column('lyric', sa.String(), nullable=True)
    image_url     = sa.Column('image_url', sa.String(), nullable=True)
    audio_url     = sa.Column('audio_url', sa.String(), nullable=True)
    video_url     = sa.Column('video_url', sa.String(), nullable=True)
    duration      = sa.Column('duration', sa.Float, server_default='0')
    source        = sa.Column('source', sa.String(), nullable=True)
    model_name    = sa.Column('model_name', sa.String(), nullable=True)
    model_version = sa.Column('model_version', sa.String(), nullable=True)

    @classmethod
    def create(cls, **kwargs):
        m_media_rec = super(Multimedia, cls).create(**kwargs)
        return m_media_rec

    @classmethod
    def select(cls, **kwargs):
        from database.model import Multimedia
        Session = SCOPED_SESSION()
        media_rec = Session.query(Multimedia).get(kwargs.get('id'))
        return media_rec