from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50),unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum('admin', 'editor', 'author', 'subscriber'), nullable=False, default='subscriber')
    status = Column(Enum('active', 'inactive', 'banned'), nullable=False, default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    meta = relationship('UserMeta', backref="user", cascade="all, delete-orphan", lazy=True)
    def __str__(self):
        return f"<User id={ self.id }, username={ self.username }, email={ self.email }, password={ self.password }, role={ self.role }, status={ self.status }, created_at={ self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at} >"