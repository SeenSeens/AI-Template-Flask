from app import db
from sqlalchemy import Column, BigInteger, Boolean, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class AiConfigFeature(db.Model):
    __tablename__ = 'ai_config_features'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    config_id = Column(BigInteger, ForeignKey('ai_configs.id', ondelete="CASCADE"), unique=True)

    is_default = Column(Boolean, default=False)
    autocomplete = Column(Boolean, default=False)
    summarize = Column(Boolean, default=False)
    translate = Column(Boolean, default=False)
    multi_chat = Column(Boolean, default=False)

    features = Column(JSON, default={})
    extra_metadata = Column(JSON, nullable=True, default={})

    # Thiết lập quan hệ ngược
    config = relationship("AiConfig", back_populates="feature_settings")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __str__(self):
        return f"<AiConfigFeatures id={self.id}, config_id={self.config_id}, is_default={self.is_default}, autocomplete={self.autocomplete}, summarize={self.summarize}, translate={self.translate}, multi_chat={self.multi_chat}, features={self.features}, extra_metadata={self.extra_metadata}, created_at={ self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
