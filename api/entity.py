from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    # One-to-many relationship with items
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
