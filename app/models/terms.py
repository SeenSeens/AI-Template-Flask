from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from app import db

class Term(db.Model):
    __tablename__ = 'terms'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __str__(self):
        return f"<Term id={self.id}, name={self.name}, slug={self.slug}, description={self.description}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
