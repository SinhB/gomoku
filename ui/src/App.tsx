import Board from "./components/Board";
import Pawn from "./components/Pawn";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Gomoku</p>
        <Pawn color="black" id={0} />
        <Pawn color="white" id={0} />
      </header>
      <body>
        <section className="board-section">
          <Board />
        </section>
      </body>
    </div>
  );
}

export default App;
