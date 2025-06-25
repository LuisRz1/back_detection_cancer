from sqlalchemy.orm import Session
from .models import SkinAnalysis

def save_analysis(db: Session, data: dict):
    analysis = SkinAnalysis(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        gender=data["gender"],
        lesion_area=data["lesionArea"],
        diagnosis=data["diagnosis"],
        confidence=data["confidence"],
        urgency=data["urgency"]
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis