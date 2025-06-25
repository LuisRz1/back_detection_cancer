from db.database import SessionLocal
from sqlalchemy import text  # ✅ Importar text correctamente

def test_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.fetchone())
    except Exception as e:
        print("Error de conexión:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
