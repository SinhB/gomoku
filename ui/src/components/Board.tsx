import Row from "./Row";

export default function Board() {
  return (
    <div>
      {[...Array(19)].map((currentElement, i) => (
        <div>
          <Row col={i} />
        </div>
      ))}
    </div>
  );
}
