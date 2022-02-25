from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import players
from app.library.helpers import *

app = FastAPI()

app.include_router(players.router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    title = "Home Page"
    return templates.TemplateResponse("index.html", {"request": request, "title": title})

