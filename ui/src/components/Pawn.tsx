export default function Pawn(props: { color: string }) {
  const { color } = props;

  return <div className={`pawn ${color}`}></div>;
}
