import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import engine  # Now this should work
from sqlmodel import SQLModel

print("🧹 Dropping all tables...")
SQLModel.metadata.drop_all(engine)
print("✅ All tables dropped.")
