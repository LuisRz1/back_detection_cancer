from sqlalchemy import Column, Integer, String, Float
from .database import Base

class SkinAnalysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    lesion_area = Column(String)
    diagnosis = Column(String)
    confidence = Column(Float)
    urgency = Column(String)
    image_path = Column(String)  # opcional
