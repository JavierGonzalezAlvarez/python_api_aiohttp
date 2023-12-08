import asyncio
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field

logger = logging.getLogger()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

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
    code: str | None
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


async def create_client(db_name: str):    
    """Beanie uses Motor async client under the hood"""    
    CONEXION_STRING = os.environ.get("CONEXION_STRING") # local entorno virtual    
    client = AsyncIOMotorClient(CONEXION_STRING)

    # create specified db
    db_created = client[db_name]
    
    # Initialize beanie with the new databa document class, create db    
    await init_beanie(
        database=db_created, document_models=[GeneralData]
    )
    
    new_address_employee = [
        {"address": "street landing", "number": "12"},
    ]

    new_address_administracion = [
        {"address": "street ocford", "number": "45"},
    ]

    new_employee = Employees(
        code_employee="EMP_01",
        status=None,
        name={"name": "peter", "first": "smith", "last": "last"},
        address_employee=new_address_employee,
    )

    new_general_data = GeneralData(
        code="0001",
        company_name="Example",
        address=new_address_administracion,
        employees=[new_employee],
    )
    
    await new_general_data.insert()

    logger.info(f"created db {db_created}")
    client.close()


async def get_current_db():
    """
      get a list of db from the cluster
    """
    CONEXION_STRING = os.environ.get("CONEXION_STRING")
    print("CONEXION:", CONEXION_STRING)
    client = AsyncIOMotorClient(CONEXION_STRING)
    try:
        database_names = await client.list_database_names()
        client.close()
        return database_names
    except Exception as e:
        logger.error(f"An error occurred while getting the database names: {e}")
        return []


async def main():
    """
    creates a new db & collection
    returns: db
    """    
    value: bool = True
    while value:
        actual_db: List = await get_current_db()  # list current db
        if actual_db is not None:
            logger.info("List of databases")
            for i in actual_db:
                print("database: ", i)
        
        db_name = input("Name of the data base: ")

        if re.match(r"\d{3}_\w+", db_name):
            # to check if db exists in mongodb
            if db_name in actual_db:
                print("DB already exist, set another name")
            else:
                value = False
        else:
            print("Invalid database name, usage: 000_name")
    
    await create_client(db_name)


if __name__ == "__main__":
    asyncio.run(main())
