from db.database import engine
from db.models import SQLModel, Asset  # Add more models here as needed

def create_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
    print("✅ Tables created successfully.")
 