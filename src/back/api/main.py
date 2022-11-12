from fastapi import Depends, FastAPI, status
from starlette.responses import JSONResponse

from src.back.api.dependencies import get_game_repository
from src.back.core.constants import PlayerTypeEnum
from src.back.domain.entities.game import Game, GameCreationRequest
from src.back.domain.repositories.game import GameRepository
from src.back.domain.schemas.game import GameBase, GameCreation

app = FastAPI()


def game_to_api_adapter(game: Game) -> GameBase:
    return GameBase(
        id=game.id,
        max_number_of_players=game.max_number_of_players,
        number_of_turns=game.number_of_turns,
        board_dimensions=game.board_dimensions,
        start_time=game.start_time,
    )


@app.post("/game/start/")
async def game_start(
    game_data: GameCreation,
    game_repository: GameRepository = Depends(get_game_repository),
):

    game_request = GameCreationRequest(**game_data.dict())
    created_game = await game_repository.start_game(game_request)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=game_to_api_adapter(created_game).dict(),
    )


@app.get("/board/turn/")
async def turn(player_type: PlayerTypeEnum, game_id: int):
    if player_type == PlayerTypeEnum.AI.value:
        return Game().ai_turn()
