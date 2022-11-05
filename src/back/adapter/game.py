from src.back.domain.repositories import GameRepository


class SQLAlchemyGameRepository(GameRepository):
    def start_game(self) -> None:
        ...

    def find_game_by_id(self, game_id: int) -> None:
        ...
