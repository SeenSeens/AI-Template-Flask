from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, Integer, Boolean, JSON, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app import db

class AiConfig(db.Model):
    __tablename__ = 'ai_configs'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider = Column(Enum('openai', 'gemini', 'anthropic', 'huggingface'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)  # Thêm khóa ngoại tới users
    model_name = Column(String(100), nullable=False)
    api_key = Column(String(255), unique=True, nullable=False)

    preset_id = Column(BigInteger, ForeignKey('ai_presets.id', ondelete='SET NULL'), nullable=True)
    preset = relationship("AiPreset", back_populates="configs")

    feature_settings = relationship("AiConfigFeature", back_populates="config", uselist=False, cascade="all, delete-orphan")

    user = relationship("User", backref="ai_configs")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    def __str__(self):
        return f"<AiConfigs id={self.id}, provider={self.provider}, user_id={self.user_id}, model_name={self.model_name}, api_key={self.api_key}, preset_id={self.preset_id}, created_at={ self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at} >"