import asyncio
import logging
import os
import re
from typing import List
import uuid

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.model import GeneralData, Employees


logger = logging.getLogger()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


async def create_client(db_name: str):    
    """Beanie uses Motor async client under the hood"""    
    CONEXION_STRING = os.environ.get("CONEXION_STRING", "mongodb://localhost:27017") # local entorno virtual    
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

    code_general = str(uuid.uuid4())
    new_general_data = GeneralData(
        code=code_general,
        company_name="Example",
        address=new_address_administracion,
        employees=[new_employee],
    )
    
    await new_general_data.insert()

    logger.info(f"created db {db_created}")
    client.close()


async def get_current_db() -> List:
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
    returns: create a db
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
