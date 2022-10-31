export interface ICell {
  coordinates: ICoordinates;
  id: number;
}

export interface ICoordinates {
  coordinates: number[];
}

export type TStone = ICoordinates & {
  id: number;
  color: string;
};

export interface IPlayerPositions {
  black: number[][];
  white: number[][];
}

export interface IFinished {
  victory: boolean;
  type: ["capture" | "alignement"];
  winner: number;
}

export interface IGameStatus {
  positions: IPlayerPositions;
  finished: IFinished;
}

export interface IGameState {
  turn: number;
  legal: boolean;
  game_status: IGameStatus;
}
