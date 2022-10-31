export default function Pawn(props: { color: string; id: number }) {
  const { color, id } = props;

  return <span className={`pawn ${color}`}>{id > 0 ? id : ""}</span>;
}
