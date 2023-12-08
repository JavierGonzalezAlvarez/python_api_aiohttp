from aiohttp import web

app = web.Application()


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hi, " + name
    return web.Response(text=text)

async def get_lits_database():
    pass

app.add_routes([
    web.get('/', handle),
    web.get('/{name}', handle)

])


if __name__ == '__main__':
    web.run_app(app)