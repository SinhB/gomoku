import "./App.css";
import Pawn from "./components/Pawn";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Gomoku</p>
        <Pawn color="black" />
        <Pawn color="white" />
      </header>
    </div>
  );
}

export default App;
