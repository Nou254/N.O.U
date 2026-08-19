"""
N.O.U Lite customer order model.

N.O.U Lite is the website's AI assistant (inspired by the WhatsApp chatbot).
It converses with customers and records orders (product purchases, project
requests, support requests) that admins review.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class NouliteOrder(Base):
    __tablename__ = "nou_lite_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # NULL when the order came from a guest (no account) - the guest's email
    # is stored in guest_email so admins can still follow up.
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    guest_email = Column(String(255), nullable=True)
    order_type = Column(String(50), nullable=False)   # product / project / support / inquiry
    summary = Column(Text, nullable=False)            # human-readable order summary from AI
    details = Column(Text)                            # structured details (JSON string)
    status = Column(String(20), default="new")        # new / in_progress / completed / cancelled
    ai_transcript = Column(Text)                      # conversation that led to the order
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("User")

    def __repr__(self):
        return f"<NouliteOrder {self.order_type} customer={self.customer_id}>"
