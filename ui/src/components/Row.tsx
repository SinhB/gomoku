import { IPlayerPositions, StoneColor } from "../types/general";
import { areArraysEqual } from "../utils";
import Stone from "./Stone";

export default function Row(props: {
  col: number;
  positions: IPlayerPositions;
}) {
  const { col, positions } = props;

  function handleClickedCoordinates(coordinate: any) {
    console.log(coordinate);
  }

  return (
    <>
      {[...Array(19)].map((currentElement, i) => (
        <div
          className="square"
          onClick={() => handleClickedCoordinates([col, i])}
          key={i}
        >
          <div className="square-content">
            {positions &&
              Object.keys(positions).map((playerColor, playerColorIdx) => {
                return (
                  <span key={`${playerColor}-${playerColorIdx}`}>
                    {positions[playerColor as StoneColor].map(
                      (stonePosition: number[], stonePositionIdx: number) => {
                        return (
                          <span key={`${stonePosition}-${stonePositionIdx}`}>
                            {areArraysEqual(stonePosition, [col, i]) && (
                              <Stone
                                color={playerColor as StoneColor}
                                id={stonePositionIdx}
                              />
                            )}
                          </span>
                        );
                      }
                    )}
                  </span>
                );
              })}
          </div>
        </div>
      ))}
    </>
  );
}
