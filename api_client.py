import aiohttp
from aiohttp import web

import asyncio
import logging
import json
from conexion import get_conexion


logger = logging.getLogger()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

client = get_conexion()

async def main():

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://0.0.0.0:8080/get_list_database') as response:

                logger.info(f"request: {response.status}")      
                logger.info("Content-type: %s", response.headers['content-type'])

                list_db = await client.list_database_names()
                client.close()

                data = json.dumps(list_db)
                logger.info(f"data: {data}")      
                                
                return web.json_response(data, content_type='application/json')

        except (TypeError, ValueError):
            raise ValueError("No conexion con el server")

asyncio.run(main())