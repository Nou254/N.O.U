"""
Question model.
"""

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Array of options [{id: 'A', text: '...'}, ...]
    correct_answer = Column(String(10), nullable=False)
    explanation = Column(Text)
    difficulty_level = Column(Integer)
    points = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    assessment_questions = relationship("AssessmentQuestion", back_populates="question")
    answers = relationship("AssessmentAnswer", back_populates="question")
    
    def __repr__(self):
        return f"<Question {self.category}>"
