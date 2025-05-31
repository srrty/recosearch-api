from sqlalchemy import Column, Integer, String, Date
from db import Base

class Paper(Base):
    __tablename__ = "papers"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String, index=True)
    authors    = Column(String)     # JSON 문자열로 직렬화하거나, 별도 테이블로 분리
    journal    = Column(String, index=True)
    pub_date   = Column(Date)
    link_url   = Column(String)
