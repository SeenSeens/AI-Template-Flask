from sqlalchemy import Column, BigInteger, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core import db

class TermTaxonomy(db.Model):
    __tablename__ = 'term_taxonomy'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    term_id = Column(BigInteger, ForeignKey('terms.id', ondelete='CASCADE'), nullable=False)
    taxonomy = Column(Enum('category', 'tag'), nullable=False)
    parent = Column(BigInteger, ForeignKey('term_taxonomy.id', ondelete='SET NULL'), nullable=True)
    # Relationships
    term = relationship("Term", backref="taxonomies", lazy=True)
    children = relationship("TermTaxonomy", backref=db.backref("parent_term", remote_side=[id]), lazy=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    def __str__(self):
        return f"<TermTaxonomy id={self.id}, term_id={self.term_id}, taxonomy={self.taxonomy}, parent={self.parent}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
