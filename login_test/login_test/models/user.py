import bcrypt
import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)
    email_confirmation_sent_on = Column(Text, nullable=True, default=0)
    email_confirmed = Column(Integer, nullable=True, default=0)
    email_confirmed_on = Column(Text, nullable=True, default=0)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        return pwhash

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw, expected_hash)  
            
        return False