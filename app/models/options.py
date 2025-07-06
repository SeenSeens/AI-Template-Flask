from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, func
from app import db

class Option(db.Model):
    __tablename__ = 'options'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    option_key = Column(String(150), unique=True, nullable=False)
    option_value = Column(Text, nullable=False)
    autoload = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    def __str__(self):
        return f"<Option id={self.id}, key={self.option_key}, value={self.option_value}, autoload={self.autoload}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"