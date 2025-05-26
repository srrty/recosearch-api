#models/bookmark.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy import String
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    paper_id   = Column(Integer, nullable=False)  # external paper ID
    paper_title  = Column(String,  nullable=False)
    paper_link   = Column(String,  nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='bookmarks')