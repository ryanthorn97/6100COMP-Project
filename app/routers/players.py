from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.library.helpers import dict2obj

from app.services.apifootball import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/player/{player_id}")
async def get_player(player_id: int, season : Optional[int] = 2021):
    squads = await getPlayerSquads(player_id)
    stats = await getPlayerStatsBySeason(player_id, season)
    #print(stats[0].statistics[0].league.name)
    data = {"squads": squads, "stats": stats}
    #print(data["squads"])
    return data

@router.get("/players/league/{league_id}")
async def get_players_stats_by_league(league_id: int, season: int, page: int):
    data = await getAllPlayerStatsInLeagueBySeason(league_id, season, page)
    return data

@router.get("/players/team/{team_id}")
async def get_players_stats_by_team(team_id: int, season: int, page: int):
    data = await getAllPlayerStatsInTeamBySeason(team_id, season, page)
    return data


#@router.get("/player/squads/{player_id}", response_class=HTMLResponse)
#async def get_player_squads(request: Request, player_id: int):
    data =  await getPlayerSquads(player_id)
    title = data[0]["players"][0]["name"]
    return templates.TemplateResponse("player.html", {"request": request, "data": data, "title": title})