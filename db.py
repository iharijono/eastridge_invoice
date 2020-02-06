#
# File                  : db.py
# Date                  : 02/05/2020
# Description           : This module drives the mapping from python objects (in model.py) to the database (sqlite).
#                         It also uses declarative extension in SQLAlchemy that
#                         allows us to define tables and models in one go, similar to how Django works.
#
#
#
# Requires              : python 3.x
#                         sqlalchemy
#
#
# Remarks               : demo code only (no production)
#
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


# Initialize the engine
engine = create_engine('sqlite:///invoices.db', convert_unicode=True)
DBSession = sessionmaker(bind=engine)
db_session = scoped_session(DBSession)
# Use declarative system

Base = declarative_base()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

def stop_db():
    # clean up db connection
    db_session.remove()

