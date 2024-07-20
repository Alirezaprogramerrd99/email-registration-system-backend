from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    letters = relationship("Letter", back_populates="owner")

class Letter(Base):
    __tablename__ = 'letters'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    sent = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="letters")