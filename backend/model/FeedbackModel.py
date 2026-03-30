from sqlalchemy import Column, Integer, String, Text, ForeignKey

from database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    content = Column(Text)
    created = Column(Integer)
    is_read = Column(Integer)

    def __init__(self, title, content, created, is_read):
        self.title = title
        self.content = content
        self.created = created
        self.is_read = is_read

    def __repr__(self):
        return (
            f"<Feedback(feedback_id={self.feedback_id}, title={self.title}, "
            f"created={self.created}, is_read={self.is_read})>"
        )
