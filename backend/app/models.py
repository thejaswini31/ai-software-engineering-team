from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    question = Column(String)
    answer = Column(String)

class UsageAnalytics(Base):

    __tablename__ = "usage_analytics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    endpoint = Column(String)

    user_id = Column(Integer)