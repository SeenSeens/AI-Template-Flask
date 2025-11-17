from sqlalchemy import Column, BigInteger, ForeignKey, PrimaryKeyConstraint, DateTime, func
from app.core import db

class PostTermRelationship(db.Model):
    __tablename__ = 'post_term_relationships'
    object_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    term_taxonomy_id = Column(BigInteger, ForeignKey('term_taxonomy.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint('object_id', 'term_taxonomy_id'),
    )

    def __str__(self):
        return f"<PostTermRelationship object_id={self.object_id}, term_taxonomy_id={self.term_taxonomy_id}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
