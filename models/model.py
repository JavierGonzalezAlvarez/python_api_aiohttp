from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from beanie import Document

class Address(BaseModel):
    """
    defines address collection
    """
    address: str | None = None
    number: str | None = None
    postal_code: str | None = None
    province: str | None = None
    state: str | None = None
    status: str | None = None  # if addresses active
    option: int | None = None  # ranking to call
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Employees(BaseModel):
    """
    defines employees collection
    """
    code_employee: str | None
    name: Dict[str, str]  # name, first, last
    category: List[str] = ["gardener"]
    status: str | None
    address_employee: List[Address] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GeneralData(Document):
    """
    define general data
    """
    code_general: str | None
    status: str = "deactivated"
    company_name: str
    juridica: Optional[List[str]] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    address: List[Address] | None = []
    employees: List[Employees] | None = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        """
        name by default of the collection
        """

        name = "general_data"

