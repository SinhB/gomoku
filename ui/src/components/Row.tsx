import { useEffect, useState } from "react";
import { IPlayerPositions } from "../types/general";
import { areArraysEqual } from "../utils";
import Stone from "./Stone";

export default function Row(props: { col: number }) {
  const [playerPositions, setPlayerPositions] = useState<IPlayerPositions>(
    {} as IPlayerPositions
  );
  const { col } = props;

  useEffect(() => {
    let originalStones = {
      black: [
        [1, 2],
        [8, 4],
        [2, 10],
      ],
      white: [
        [5, 6],
        [2, 8],
        [8, 18],
      ],
    };
    setPlayerPositions(originalStones);
  }, []);

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
            {Object.keys(playerPositions).map(
              (playerColor: string, idx: number) => {
                return (
                  <>
                    {playerPositions[playerColor as keyof IPlayerPositions].map(
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
              }
            )}
          </div>
        </div>
      ))}
    </>
  );
}
