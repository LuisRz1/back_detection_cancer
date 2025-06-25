from app.db import models

def save_analysis(db, data: dict):
    analysis = models.SkinAnalysis(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        gender=data["gender"],
        lesion_area=data["lesion_area"],
        diagnosis=data["diagnosis"],
        image=data["image"]
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis
