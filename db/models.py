from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
import datetime
import enum

class AssetStatus(str, enum.Enum):
    in_use = "In Use"
    under_maintenance = "Under Maintenance"
    retired = "Retired"

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
