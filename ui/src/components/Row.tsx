import { useEffect, useState } from "react";
import { IStone } from "../types/general";
import { areArraysEqual } from "../utils";
import Stone from "./Stone";

export default function Row(props: { col: number }) {
  const [stones, setStones] = useState<IStone[]>([]);
  const { col } = props;

  useEffect(() => {
    let originalStones = [{ id: 1, color: "black", coordinates: [2, 5] }];
    setStones(originalStones);
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
            {stones?.map(
              (pawn) =>
                areArraysEqual(pawn.coordinates, [col, i]) && (
                  <Stone color={pawn.color} id={pawn.id} />
                )
            )}
          </div>
        </div>
      ))}
    </>
  );
}
