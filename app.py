import os

import openai

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from myapp.routes import about, home
from myapp.utils.utils import Utils

# Define the API key
openaiKey = os.getenv("OPENAI_API_KEY")

# Initialize the app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register the routers
app.include_router(about.router)
app.include_router(home.router)

@app.on_event("startup")
async def startup_event():
    home.register_home_path(app)
    about.register_about_path(app)
    templates.env.globals["url_path_for"] = app.url_path_for
    openai.api_key = openaiKey

