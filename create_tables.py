from models import SQLModel, engine

def recreate_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    recreate_tables()
