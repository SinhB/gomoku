import Board from "./components/Board";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Gomoku</p>
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
