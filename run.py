import asyncio
import logging
from aiohttp import web
from api_v1.routes import setup_routes
from api_v1.src.scheduler import Scheduler
from api_v1.main import init_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_server():
    app = init_app()
    host = '127.0.0.1'
    port = 8080
    logger.info(f"Starting server on {host}:{port}")
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    try:
        run_server()
    except (SystemExit, KeyboardInterrupt):
        logger.info("Shutting down the server.")
