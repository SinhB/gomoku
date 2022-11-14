from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.back.api.dependencies import get_game_repository
from src.back.core.constants import PlayerTypeEnum
from src.back.domain.entities.game import Game, GameCreationRequest
from src.back.domain.repositories.game import GameRepository
from src.back.domain.schemas.game import GameBase, GameCreation
from src.back.use_cases import StartGameUseCase

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def game_to_api_adapter(game: Game) -> GameBase:
    print(game)
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
    use_case = StartGameUseCase(game_repository)
    created_game = await use_case(game_request)

    return created_game


@app.get("/game/find/{game_id}")
async def game_find_by_id(
    game_id: int,
    game_repository: GameRepository = Depends(get_game_repository),
):
    found_game = await game_repository.find_game_by_id(game_id)

    return found_game


@app.get("/board/turn/")
async def turn(player_type: PlayerTypeEnum, game_id: int):
    if player_type == PlayerTypeEnum.AI.value:
        return Game().ai_turn()
