import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from app import app

from dotenv import load_dotenv
import os
load_dotenv()

config = Config()
config.bind = [os.getenv("BIND")+":"+os.getenv("PORT")]
config.loglevel = "info"
config.use_reloader = True
config.reload_dirs = ["app"]
config.worker_class = "trio"
asyncio.run(serve(app, config))