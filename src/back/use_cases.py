from src.back.domain.schemas.game import PlacingStone


class PlacingStone:
    def __call__(self, stone: PlacingStone) -> None:
        ...
