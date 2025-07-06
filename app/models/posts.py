from sqlalchemy import Column, String, BigInteger, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from app import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(LONGTEXT, nullable=True)
    excerpt = Column(Text, nullable=True)
    status = Column(Enum('publish', 'draft', 'pending', 'private', 'trash'), nullable=False, default='draft')
    type = Column(Enum('post', 'page'), nullable=False, default='post')
    author_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    author = relationship('User', backref='posts', lazy=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __str__(self):
        return f"<Post id={self.id}, title={self.title}, slug={self.slug}, content={self.content}, excerpt={self.excerpt}, status={self.status}, type={self.type}, author_id={self.author_id}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
