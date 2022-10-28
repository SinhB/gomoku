export interface ICell {
  coordinates: ICoordinates;
  id: number;
}

export interface ICoordinates {
  coordinates: number[];
}

export type IPawn = ICoordinates & {
  id: number;
  color: string;
};
