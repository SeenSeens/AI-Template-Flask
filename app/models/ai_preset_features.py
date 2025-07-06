from app import db
from sqlalchemy import Column, BigInteger, Boolean, JSON, DateTime, func
from sqlalchemy.orm import relationship

class AiPresetFeature(db.Model):
    __tablename__ = 'ai_preset_features'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    preset_id = db.Column(db.BigInteger, db.ForeignKey('ai_presets.id'), nullable=False, unique=True)
    is_default = Column(Boolean, default=False)
    autocomplete = Column(Boolean, default=False)
    summarize = Column(Boolean, default=False)
    translate = Column(Boolean, default=False)
    multi_chat = Column(Boolean, default=False)
    features = Column(JSON, default={})
    extra_metadata = Column(JSON, nullable=True, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Thiết lập quan hệ ngược
    preset = relationship("AiPreset", back_populates="features")

    def __str__(self):
        return f"<AiConfigFeatures id={self.id}, is_default={self.is_default}, autocomplete={self.autocomplete}, summarize={self.summarize}, translate={self.translate}, multi_chat={self.multi_chat}, features={self.features}, extra_metadata={self.extra_metadata}, created_at={ self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
