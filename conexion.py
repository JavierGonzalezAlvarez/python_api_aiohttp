import os
from motor.motor_asyncio import AsyncIOMotorClient

CONEXION_STRING = os.environ.get("CONEXION_STRING", "mongodb://localhost:27017") # local entorno virtual    

def get_conexion():    
    print("CONEXION:", CONEXION_STRING)
    client = AsyncIOMotorClient(CONEXION_STRING)
    return client