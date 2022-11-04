from fastapi import FastAPI
from src.back.core.constants import PlayerTypeEnum
from src.game import Game

app = FastAPI()


@app.get("/game/start/")
async def game_start():
    Game().start()


@app.get("/board/turn/")
async def turn(player_type: PlayerTypeEnum, game_id: int):
    if player_type == PlayerTypeEnum.AI.value:
        return Game().ai_turn()
