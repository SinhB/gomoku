import { useEffect, useState } from "react";
import { IPawn } from "../types/general";
import { areArraysEqual } from "../utils";
import Pawn from "./Pawn";

export default function Row(props: { col: number }) {
  const [pawns, setPawns] = useState<IPawn[]>([]);
  const { col } = props;

  useEffect(() => {
    let originalPawns = [{ id: 1, color: "black", coordinates: [2, 5] }];
    setPawns(originalPawns);
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
            {pawns?.map(
              (pawn) =>
                areArraysEqual(pawn.coordinates, [col, i]) && (
                  <Pawn color={pawn.color} id={pawn.id} />
                )
            )}
          </div>
        </div>
      ))}
    </>
  );
}
