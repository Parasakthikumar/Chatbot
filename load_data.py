import csv
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models import (
    Department,
    Employee,
    Asset,
    MaintenanceLog,
    Vendor,
    AssetVendorLink
)

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def load_csv_data(filename):
    """Load and clean CSV data."""
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            cleaned_row = {
                k: (v.strip() if v and v.strip() != "" else None) for k, v in row.items()
            }

            # Convert numeric IDs (but skip UUIDs)
            if 'id' in cleaned_row and cleaned_row['id'] and cleaned_row['id'].isdigit():
                cleaned_row['id'] = int(cleaned_row['id'])

            data.append(cleaned_row)
        return data

def main():
    print("🚀 Starting data load...")

    session = Session()
    try:
        print("🧹 Deleting old data...")
        session.execute(text("DELETE FROM assetvendorlink"))
        session.execute(text("DELETE FROM maintenancelog"))
        session.execute(text("DELETE FROM asset"))
        session.execute(text("DELETE FROM employee"))
        session.execute(text("DELETE FROM department"))
        session.execute(text("DELETE FROM vendor"))
        session.commit()

        print("📥 Loading CSV data...")
        departments_data = load_csv_data("sample_data/departments.csv")
        employees_data = load_csv_data("sample_data/employees.csv")
        assets_data = load_csv_data("sample_data/assets.csv")
        maintenance_logs_data = load_csv_data("sample_data/maintenance_logs.csv")
        vendors_data = load_csv_data("sample_data/vendors.csv")
        asset_vendor_links_data = load_csv_data("sample_data/asset_vendor_links.csv")

        print("📝 Inserting data into tables...")
        session.bulk_insert_mappings(Department, departments_data)
        session.bulk_insert_mappings(Employee, employees_data)
        session.bulk_insert_mappings(Asset, assets_data)
        session.bulk_insert_mappings(MaintenanceLog, maintenance_logs_data)
        session.bulk_insert_mappings(Vendor, vendors_data)
        session.bulk_insert_mappings(AssetVendorLink, asset_vendor_links_data)

        session.commit()
        print("✅ Data loaded successfully!")

    except Exception as e:
        session.rollback()
        print(f"❌ Error during data load: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
