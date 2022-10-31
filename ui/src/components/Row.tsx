import { IPlayerPositions } from "../types/general";
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
        >
          <div>
            {positions &&
              Object.keys(positions).map((playerColor: string, idx: number) => {
                return (
                  <>
                    {positions[playerColor as keyof IPlayerPositions].map(
                      (stonePosition: number[], index: number) => {
                        return (
                          <>
                            {areArraysEqual(stonePosition, [col, i]) && (
                              <Stone color={playerColor} id={index} />
                            )}
                          </>
                        );
                      }
                    )}
                  </>
                );
              })}
          </div>
        </div>
      ))}
    </>
  );
}
