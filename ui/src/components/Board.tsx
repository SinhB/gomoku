import Row from "./Row";

export default function Board() {
  return (
    <div className="board">
      <div className="container">
        {[...Array(19)].map((currentElement, i) => (
          <>
            <Row col={i} />
          </>
        ))}
      </div>
    </div>
  );
}
