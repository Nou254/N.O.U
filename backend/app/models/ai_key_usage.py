"""
AI key usage tracking for the Groq key pool.

Tracks, per day and per AI section, which Groq API keys have been used and
how many requests each key served. The pool service (app/services/groq_pool.py)
uses this to enforce the product rules:

- 60 Groq API keys in total (configured in .env),
- each AI section (assessments, N.O.U Lite, project chat) gets **10 keys per day**,
- if a section depletes its 10 keys, it is topped up with **2 more** for the day,
- keys that fail (401/expired) are skipped for the rest of the day.
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class AIKeyUsage(Base):
    __tablename__ = "ai_key_usage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usage_date = Column(Date, nullable=False, index=True)
    section = Column(String(50), nullable=False, index=True)  # assessments / nou_lite / project_chat
    key_index = Column(Integer, nullable=False)               # index into settings.GROQ_API_KEYS
    requests = Column(Integer, default=0)                     # requests served by this key today
    failed = Column(Boolean, default=False)                   # key hit an auth/expiry error -> skip today
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<AIKeyUsage {self.usage_date} {self.section} key#{self.key_index}>"
