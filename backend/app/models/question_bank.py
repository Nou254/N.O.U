"""
Question bank model - pre-generated assessment questions.

Groq generates 100 advanced, real-world, open-ended questions per
professional category (20 per assessment part: common/category/position/
practical/professional) ahead of time. Each assessment then selects 20
questions AT RANDOM from the category's bank, so exam starts are instant and
every applicant receives a randomized set. Groq is never called while the
applicant is taking the exam - it is only used afterwards to grade the
answers and to review CVs for the admin.
"""

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class QuestionBankQuestion(Base):
    __tablename__ = "question_bank"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # The professional category this question belongs to (a question bank is
    # generated per category, not per position).
    category_id = Column(
        Integer, ForeignKey("personnel_categories.id"), nullable=False, index=True
    )
    category_name = Column(String(120), nullable=False)
    # Which of the 5 assessment parts this question tests (common/category/
    # position/practical/professional) - keeps the weighted scoring model.
    part = Column(String(30), nullable=False, index=True)
    # Question type (NO MCQs): short_answer / written_explanation / scenario /
    # practical / debugging / design / project.
    question_type = Column(String(30), nullable=False, default="written_explanation")
    question_text = Column(Text, nullable=False)
    # Key points a strong answer must cover (used to focus Groq's grading).
    grading_notes = Column(Text)
    points = Column(Integer, nullable=False, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<QuestionBankQuestion {self.category_name} {self.part} #{self.id}>"
