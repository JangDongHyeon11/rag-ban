import os
import json
import logging
import fastapi
import sqlalchemy
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from .db_tables import Base, APILogTable

logger = logging.getLogger('main')

POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_API_LOG_TABLE_NAME = os.getenv('DB_API_LOG_TABLE_NAME', 'api_log')
DB_CONNECTION_URL = os.getenv('DB_CONNECTION_URL', f'postgresql://dl_user:pgadmin123@postgres:{POSTGRES_PORT}/dl_pg_db')
print(DB_CONNECTION_URL)
required_db_tables = [ DB_API_LOG_TABLE_NAME]

def prepare_db() -> None:
    logger.info("Preparing database")
    engine = create_engine(DB_CONNECTION_URL)
    Base.metadata.create_all(engine)
    logger.info("Database is ready.")

def check_db_healthy() -> None:
    engine = create_engine(DB_CONNECTION_URL)
    with engine.connect() as connection:
        result = connection.execute(text(f"select 1 from {DB_API_LOG_TABLE_NAME} limit 1"))
        result.all()

def open_db_session(engine: sqlalchemy.engine) -> sqlalchemy.orm.Session:
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    
def create_api_log_entry(request_obj: fastapi.Request, resp_code: int, resp_message: str, timespan: float,) -> APILogTable:
    entry = APILogTable(request_method=str(request_obj.method), request_url=str(request_obj.url),
                        response_status_code=resp_code, response_message=resp_message, timespan=timespan)
    return entry


def commit_only_api_log_to_db(request_obj: fastapi.Request, resp_code: int, resp_message: str, timespan: float) -> None:
    engine = create_engine(DB_CONNECTION_URL)
    session = open_db_session(engine)
    record = create_api_log_entry(request_obj, resp_code, resp_message, timespan)
    session.add(record)
    session.commit()
    session.close()