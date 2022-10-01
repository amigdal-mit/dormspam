from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from server.models import Base
import datetime
import secrets


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True,
                unique=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="clients")

    uid = Column(String(255), unique=True)
    token = Column(String(255))

    date_created = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, user):
        self.user = user
        self.generate_uniques()
        self.token = secrets.token_hex(32)

    def generate_uniques(self):
        self.uid = secrets.token_hex(32)
