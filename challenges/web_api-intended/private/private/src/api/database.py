#! /usr/bin/env python3

# DB helpers for creating and operating on database


import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.getenv('DB_FILE')}"
SQLALCHEMY_DATABASE_URL = f"sqlite:////tmp/sqlite-web-intended.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

