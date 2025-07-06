from sqlalchemy import BigInteger, Column, ForeignKey, String, Text, UniqueConstraint, DateTime, func
from app import db

class UserMeta(db.Model):
    __tablename__ = 'user_meta'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)  # dùng string 'users.id'
    meta_key = Column(String(50))
    meta_value = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (
        UniqueConstraint('user_id', 'meta_key', name='uq_user_meta'),
    )

    def __str__(self):
        return f"<UserMeta id={self.id}, user_id={self.user_id}, meta_key={self.meta_key}, meta_value={self.meta_value}, created_at = { self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
