import { useEffect, useState } from "react";
import { IPawn } from "../types/general";
import EmptySpace from "./EmptySpace";
import Pawn from "./Pawn";

export default function Row(props: { col: number }) {
  const [pawns, setPawns] = useState<IPawn[]>();

  useEffect(() => {
    let originalPawns = [{ id: 1, color: "black", coordinates: [0, 0] }];
    setPawns(originalPawns);
  }, []);

  const { col } = props;

  return (
    <div>
      {[...Array(19)].map((cell, i) => (
        <span key={cell}>
          {pawns?.map((pawn, i) => (
            <span key={pawn.id}>
              {pawn.id == 1 ? (
                <Pawn color="black" />
              ) : (
                <>
                  <EmptySpace />
                </>
              )}
            </span>
          ))}
        </span>
      ))}
    </div>
  );
}
