from sqlalchemy import Column, Integer, String, LargeBinary
from app.db.database import Base

class SkinAnalysis(Base):
    __tablename__ = "skin_analysis"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    lesion_area = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)

