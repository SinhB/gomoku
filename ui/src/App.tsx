import { startGame } from "./api/game";
import Board from "./components/Board";
import Button from "./components/Button";
import Stone from "./components/Stone";

const gameCreationDefault = {
  players: [{ color: "black" }, { color: "white" }],
  max_number_of_players: 2,
  number_of_turns: 0,
  board_dimensions: "19x19",
};

function App() {
  return (
    <>
      <section className="App">
        <header className="App-header">
          G<Stone color="black" id={-1} />M<Stone color="white" id={-1} />
          KU
        </header>
      </section>
      <div>
        <section className="center mb-5">
          <Button onclick={startGame} params={gameCreationDefault}>
            Start
          </Button>
        </section>
        <section className="board-section">
          <Board />
        </section>
      </div>
    </>
  );
}

export default App;
