from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request

from threading import Thread

from utils.env import env
from utils.slack import app
from utils.queue import process_queue


async def ping(request):
    return JSONResponse({"status": "OK", "message": "App is running"})


app_handler = AsyncSlackRequestHandler(app)


async def endpoint(req: Request):
    return await app_handler.handle(req)


queue_thread = Thread(target=process_queue, daemon=True).start()
api = Starlette(
    debug=True,
    routes=[
        Route("/slack/events", endpoint=endpoint, methods=["POST"]),
        Route("/ping", endpoint=ping, methods=["GET"]),
    ],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:api", host="0.0.0.0", port=env.port, log_level="info")
