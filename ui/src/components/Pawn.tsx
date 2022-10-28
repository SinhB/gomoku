export default function Pawn(props: { color: string; id: number }) {
  const { color, id } = props;

  return <div className={`pawn ${color}`}>{id}</div>;
}
