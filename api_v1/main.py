from aiohttp import web
from api_v1.routes import setup_routes
from api_v1.src.scheduler import Scheduler


def init_app():
    app = web.Application()
    setup_routes(app)

    app['scheduler'] = Scheduler()

    return app
