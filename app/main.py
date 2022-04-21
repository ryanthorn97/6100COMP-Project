from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import players, teams, competitions
from app.library import helpers

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(competitions.router)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    title = "Home Page"
    return templates.TemplateResponse("index.html", {"request": request, "title": title})


#for x in range(2010, 2022):
    #teams.addAllTeams(39, x)
    #teams.addAllTeams(140, x)
    #teams.addAllTeams(78, x)
    #teams.addAllTeams(61, x)
    #teams.addAllTeams(135, x)

    #teams.addAllcompetitionStandings(39, x)
    #teams.addAllcompetitionStandings(140, x)
    #teams.addAllcompetitionStandings(78, x)
    #teams.addAllcompetitionStandings(61, x)
    #teams.addAllcompetitionStandings(135, x)

#players.addAllPlayers(276)
#players.getAllPlayerIDs()

#print(helpers.num_sim(100, 89))