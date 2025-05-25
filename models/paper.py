from sqlalchemy import Column, Integer, String, Text
from db import Base

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    authors = Column(Text)
    journal = Column(String)
    url = Column(String)