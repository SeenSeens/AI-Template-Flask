from app import db
from sqlalchemy import Column, String, Float, Integer, BigInteger, DateTime, func, Enum

class AiPreset(db.Model):
    __tablename__ = 'ai_presets'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    use_case = Column(String(50), nullable=False, unique=True)  # ví dụ: "content_writing", "coding", ...
    type = Column(Enum('content', 'image', 'design', 'audio', 'video', 'other'), default='content', nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    top_p = Column(Float, nullable=False, default=1.0)
    max_tokens = Column(Integer, nullable=False, default=512)
    frequency_penalty = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    config_links = db.relationship("AiConfigPreset", back_populates="preset", cascade="all, delete-orphan")
    features = db.relationship("AiPresetFeature", back_populates="preset", uselist=False, cascade="all, delete-orphan")

    def __str__(self):
        return f"<AiPreset id={self.id}, use_case={self.use_case}, temperature={self.temperature}, top_p={self.top_p}, max_tokens={self.max_tokens}, frequency_penalty={self.frequency_penalty}, created_at={ self.created_at }, updated_at={self.updated_at}, deleted_at={self.deleted_at}>"
