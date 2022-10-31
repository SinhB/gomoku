import Board from "./components/Board";
import Stone from "./components/Stone";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Gomoku</p>
        <Stone color="black" id={0} />
        <Stone color="white" id={0} />
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
