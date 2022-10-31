import Board from "./components/Board";
import Stone from "./components/Stone";

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
        <section className="board-section">
          <Board />
        </section>
      </div>
    </>
  );
}

export default App;
