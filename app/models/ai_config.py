from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, Integer, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from app import db

class AiConfigs(db.Model):
    __tablename__ = 'ai_configs'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider = Column(Enum('openai', 'gemini', 'anthropic', 'huggingface'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)  # Thêm khóa ngoại tới users
    model_name = Column(String(100), nullable=False)
    api_key = Column(String(255), unique=True, nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    top_p = Column(Float, nullable=False, default=1.0)
    max_tokens = Column(Integer, nullable=False, default=512)
    frequency_penalty = Column(Float, nullable=False, default=0.0)
    features = Column(JSON, default={})
    extra_metadata = Column(JSON, nullable=True, default={})
    is_default = Column(Boolean, default=False)
    autocomplete = Column(Boolean, default=False)
    summarize = Column(Boolean, default=False)
    translate = Column(Boolean, default=False)
    multi_chat = Column(Boolean, default=False)
    user = relationship("User", backref="ai_configs")

    def __str__(self):
        return f"<AiConfigs id={self.id}, provider={self.provider}, user_id={self.user_id}, model_name={self.model_name}, api_key={self.api_key}, temperature={self.temperature}, top_p={self.top_p}, max_tokens={self.max_tokens}, frequency_penalty={self.frequency_penalty}, features={self.features}, extra_metadata={self.extra_metadata}, is_default={self.is_default}, autocomplete={self.autocomplete}, summarize={self.summarize}, translate={self.translate}, multi_chat={self.multi_chat}, user={self.user} >"