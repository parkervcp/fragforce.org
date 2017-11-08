""" Database schema

WARNING: DON'T FORGET TO RUN 'alembic revision --autogenerate -m "<message>"' AFTER ANY CHANGES TO THE SCHEMA!!!!
"""
import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation, backref, deferred
from sqlalchemy.dialects.postgresql import UUID, ENUM, HSTORE, ARRAY, JSONB
from fragforce import app, Base, RemoteBaseMeta, engine
import uuid

