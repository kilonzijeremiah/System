from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
