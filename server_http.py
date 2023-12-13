import json
import os
from typing import List
from aiohttp import web
import logging
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

app = web.Application()

CONEXION_STRING = os.environ.get("CONEXION_STRING", "mongodb://localhost:27017") # local entorno virtual    
client = AsyncIOMotorClient(CONEXION_STRING)

async def handle(request):    
    logger.info(f"request: {request}")
    name = request.match_info.get('name', "this is a pure web api - no frameworks")
    text = "Hi, " + name
    return web.Response(text=text)


async def get_list_database(request) -> List:  
    list_db = await client.list_database_names()
    data = json.dumps(list_db)
    logger.info(f"data: {data}")
    return web.Response(text=data, content_type='application/json')


app.add_routes([
    web.get('/', handle),
    web.get('/get_list_database', get_list_database),     
    web.get('/{name}', handle), # wildcard, must be at the end           
])


if __name__ == '__main__':
    web.run_app(app)