from sqlalchemy import Column, func, BigInteger, DateTime, ForeignKey

from app import db

class AIConfigPreset(db.Model):
    __tablename__ = 'ai_config_presets'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    config_id = Column(BigInteger, ForeignKey('ai_configs.id'), nullable=False)
    preset_id = Column(BigInteger, ForeignKey('ai_presets.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    config = db.relationship("AIConfig", back_populates="presets")
    preset = db.relationship("AIPreset", back_populates="config_links")
