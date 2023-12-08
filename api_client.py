import aiohttp
from aiohttp import web

import asyncio
import logging
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

CONEXION_STRING = os.environ.get("CONEXION_STRING", "mongodb://localhost:27017") # local entorno virtual    
client = AsyncIOMotorClient(CONEXION_STRING)

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://0.0.0.0:8080/get_list_database') as response:

            logger.info(f"request: {response.status}")      
            logger.info("Content-type: %s", response.headers['content-type'])

            list_db = await client.list_database_names()
            data = json.dumps(list_db)
            logger.info(f"data: {data}")      
            
            return web.json_response(data, content_type='application/json')


asyncio.run(main())