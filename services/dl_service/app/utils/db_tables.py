import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

DB_API_LOG_TABLE_NAME = os.getenv('DB_API_LOG_TABLE_NAME', 'api_log')

class APILogTable(Base):
    __tablename__ = DB_API_LOG_TABLE_NAME
    id = Column(Integer, primary_key=True)
    request_method = Column(String)
    request_url = Column(String)
    response_status_code = Column(Integer)
    response_message = Column(String)
    timespan = Column(Float)
    created_on = Column(DateTime, default=datetime.now)


