# Every Models Represnt Table....
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# For Table Creation:
class Post(Base):
    __tablename__ = "posts"

    # Columns Name:
    id  = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)   # By Default it takes True if not provide then...
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("user_data.id", ondelete="CASCADE"), nullable=False)   # After Adding
    user = relationship("User")   # For Connect the Post Table with User Table for Inner Join example....
    # votes = relationship("Votes", back_populates="posts")


class User(Base):
    __tablename__ = "user_data"

    id  = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    phone_no = Column(String)


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_data.id", ondelete="CASCADE"), primary_key=True, nullable=False)   
    # post = relationship("Post", back_populates="votes") 