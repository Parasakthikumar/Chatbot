from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional, List
import uuid
import datetime
import enum
import os
from dotenv import load_dotenv

# ---------------- Enums ----------------
class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

# ---------------- Department ----------------
class Department(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    location: str

    employees: List["Employee"] = Relationship(back_populates="department")
    assets: List["Asset"] = Relationship(back_populates="department")

# ---------------- Employee ----------------
class Employee(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str
    phone: str
    department_id: uuid.UUID = Field(foreign_key="department.id")

    department: Optional[Department] = Relationship(back_populates="employees")
    assets: List["Asset"] = Relationship(back_populates="assigned_employee")

# ---------------- Asset ----------------
class Asset(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    asset_tag: str
    name: str
    category: str
    location: str
    purchase_date: datetime.date
    warranty_until: datetime.date
    assigned_to: Optional[uuid.UUID] = Field(default=None, foreign_key="employee.id")
    department_id: uuid.UUID = Field(foreign_key="department.id")
    status: AssetStatus

    assigned_employee: Optional[Employee] = Relationship(back_populates="assets")
    department: Optional[Department] = Relationship(back_populates="assets")
    maintenance_logs: List["MaintenanceLog"] = Relationship(back_populates="asset")
    vendor_links: List["AssetVendorLink"] = Relationship(back_populates="asset")

# ---------------- Vendor ----------------
class Vendor(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    contact_email: str
    contact_phone: str
    address: str

    asset_links: List["AssetVendorLink"] = Relationship(back_populates="vendor")

# ---------------- Asset-Vendor Link Table ----------------
class AssetVendorLink(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id")
    vendor_id: uuid.UUID = Field(foreign_key="vendor.id")
    service_type: str
    contract_start: datetime.date
    contract_end: datetime.date

    asset: Optional[Asset] = Relationship(back_populates="vendor_links")
    vendor: Optional[Vendor] = Relationship(back_populates="asset_links")

# ---------------- Maintenance Logs ----------------
class MaintenanceLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id")
    service_date: datetime.date
    issue_reported: str
    action_taken: str
    cost: float
    serviced_by: str

    asset: Optional[Asset] = Relationship(back_populates="maintenance_logs")

# ---------------- Engine Setup ----------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
