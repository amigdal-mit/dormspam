from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from server.models import Base
import datetime
import secrets


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,
                unique=True, autoincrement=True)

    email = Column(String(255), unique=True, primary_key=True)

    admin_is = Column(Boolean, default=False)
    
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_updated = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, email):
        self.email = email

    def json(self):
        return {
            'admin_is': self.admin_is
        }