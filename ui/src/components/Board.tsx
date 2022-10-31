import { useEffect, useState } from "react";
import { IGameState } from "../types/general";
import Row from "./Row";

export default function Board() {
  const [gameState, setGameState] = useState<IGameState>({} as IGameState);

  useEffect(() => {
    let originalGameState = {
      turn: 10,
      legal: false,
      gameStatus: {
        positions: {
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
        },
        finished: {
          victory: false,
          type: null,
          winner: -1,
        },
        players: {
          black: {
            score: 0,
            stones: 0,
          },
          white: {
            score: 0,
            stones: 0,
          },
        },
      },
    };
    setGameState(originalGameState);
    console.log(originalGameState);
  }, []);

  return (
    <div className="board">
      <div className="container">
        {[...Array(19)].map((currentElement, i) => (
          <div key={i}>
            <Row col={i} positions={gameState?.gameStatus?.positions} />
          </div>
        ))}
      </div>
    </div>
  );
}
