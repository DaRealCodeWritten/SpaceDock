"""Add Mod.score

Revision ID: 85be165bc5dc
Revises: d6f41a805840
Create Date: 2020-06-23 17:49:36.709613

"""

# revision identifiers, used by Alembic.
from datetime import datetime
from time import sleep

from sqlalchemy import orm, Column, Integer, Unicode, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from KerbalStuff.celery import calculate_mod_scores
from KerbalStuff.search import get_mod_score

revision = '85be165bc5dc'
down_revision = 'd6f41a805840'

from alembic import op
import sqlalchemy as sa


Base = declarative_base()


class Mod(Base):
    __tablename__ = 'mod'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now)
    description = Column(Unicode(100000))
    source_link = Column(String(256))
    follower_count = Column(Integer, nullable=False, default=0)
    download_count = Column(Integer, nullable=False, default=0)
    score = Column(sa.Float, default=0, nullable=False, index=True)


class ModVersion(Base):
    __tablename__ = 'modversion'
    id = Column(Integer, primary_key=True)
    mod_id = Column(Integer, ForeignKey('mod.id'))
    mod = relationship('Mod',
                       backref=backref('versions', order_by="desc(ModVersion.sort_index)"),
                       foreign_keys=mod_id)
    sort_index = Column(Integer, default=0)


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    mod_id = Column(Integer, ForeignKey('mod.id'))
    mod = relationship('Mod', backref=backref('media', order_by=id))


def upgrade():
    # autogenerated
    op.add_column('mod', sa.Column('score', sa.Float(), nullable=False, index=True, server_default='0'))

    # manually added
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for mod in session.query(Mod).all():
        mod.score = get_mod_score(mod)

    session.commit()


def downgrade():
    # autogenerated
    op.drop_column('mod', 'score')