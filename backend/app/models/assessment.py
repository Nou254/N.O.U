"""
Assessment models.
"""

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False, default=60)
    total_questions = Column(Integer, nullable=False, default=50)
    passing_score = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    assessment_questions = relationship("AssessmentQuestion", back_populates="assessment")
    sessions = relationship("AssessmentSession", back_populates="assessment")
    
    def __repr__(self):
        return f"<Assessment {self.title}>"


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    order_number = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False, default=1)
    
    # Relationships
    assessment = relationship("Assessment", back_populates="assessment_questions")
    question = relationship("Question", back_populates="assessment_questions")
    
    def __repr__(self):
        return f"<AssessmentQuestion {self.order_number}>"


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    time_remaining = Column(Integer)  # in seconds
    score = Column(Numeric(5, 2))
    percentage = Column(Numeric(5, 2))
    status = Column(String(20), default="in_progress")
    ip_address = Column(String(45))
    user_agent = Column(Text)
    ai_summary = Column(Text)             # AI overall assessment (open-ended)
    ai_recommendation = Column(String(50))  # PASS / FAIL (see assessment_modules)
    modules = Column(Text)                # JSON list of selected module names
    results_emailed_at = Column(DateTime) # set once results email is sent
    # ---- N.O.U. assessment framework (today.md) ----
    # The applicant's selected professional category and position.
    category_id = Column(Integer, ForeignKey("personnel_categories.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("personnel_positions.id"), nullable=True)
    category_name = Column(String(120), nullable=True)
    position_name = Column(String(120), nullable=True)
    # Per-part percentage scores, JSON: {part: percentage}.
    part_scores = Column(Text)
    # Competency band: Not Qualified / Developing / Competent /
    # N.O.U. Qualified / Advanced (today.md sec. 6).
    competency_band = Column(String(30), nullable=True)
    # Alternative professional category recommended when the applicant does
    # not qualify for the applied position (today.md sec. 41).
    recommended_category = Column(String(120), nullable=True)
    # Developer onboarding: an admin approves passed applicants; the applicant
    # is then invited with new login credentials to the projects portal.
    onboarding_status = Column(String(20), default="pending")  # pending / approved / declined
    onboarding_decided_at = Column(DateTime)
    onboarding_notes = Column(Text)
    
    # Relationships
    applicant = relationship("User", back_populates="assessment_sessions")
    assessment = relationship("Assessment", back_populates="sessions")
    answers = relationship("AssessmentAnswer", back_populates="session")
    session_questions = relationship("AssessmentSessionQuestion", back_populates="session")
    
    def __repr__(self):
        return f"<AssessmentSession {self.id}>"


class AssessmentSessionQuestion(Base):
    """
    Snapshot of an AI-generated question for a specific assessment session.

    AI questions are generated fresh per candidate (advanced, randomized
    across the entire tech world) and are intentionally never stored in the
    shared question bank - each session owns its own copy.
    """

    __tablename__ = "assessment_session_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)
    module = Column(String(100), nullable=False, default="General")
    # Which of the 5 parts this question belongs to (common/category/position/
    # practical/professional).
    part = Column(String(30), default="position", index=True)
    # Question type (NO MCQs): short_answer / written_explanation / scenario /
    # practical / debugging / design / project.
    question_type = Column(String(30), default="written_explanation")
    question_text = Column(Text, nullable=False)
    order_number = Column(Integer, nullable=False)
    points = Column(Integer, default=10)
    grading_notes = Column(Text)

    # Relationships
    session = relationship("AssessmentSession", back_populates="session_questions")
    answers = relationship("AssessmentAnswer", back_populates="session_question")

    def __repr__(self):
        return f"<AssessmentSessionQuestion {self.order_number}>"


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=True)
    session_question_id = Column(
        Integer, ForeignKey("assessment_session_questions.id", ondelete="CASCADE"), nullable=True
    )
    user_answer = Column(Text)  # open-ended written answers for AI sessions
    is_correct = Column(Boolean)
    points_earned = Column(Integer, default=0)
    ai_feedback = Column(Text)
    answered_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    session = relationship("AssessmentSession", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    session_question = relationship("AssessmentSessionQuestion", back_populates="answers")
    
    def __repr__(self):
        return f"<AssessmentAnswer {self.id}>"
