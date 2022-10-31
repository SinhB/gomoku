export type StoneColor = "black" | "white";

export type FinishedType = "capture" | "alignement" | null;

export interface IStone {
  id: number;
  color: StoneColor;
}

export interface ICell {
  id: number;
  coordinates: ICoordinates;
}

export interface ICoordinates {
  coordinates: number[];
}

export interface IPlayerPositions {
  [StoneColor: string]: number[][];
}

export interface IPlayerGameState {
  [score: string]: number;
  stones: number;
}

export interface IPlayersGameState {
  [StoneColor: string]: IPlayerGameState;
}

export interface IFinished {
  victory: boolean;
  type: FinishedType;
  winner: number;
}

export interface IGameStatus {
  positions: IPlayerPositions;
  finished: IFinished;
}

export interface IGameState {
  turn: number;
  legal: boolean;
  gameStatus: IGameStatus;
}
