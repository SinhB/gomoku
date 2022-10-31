export default function Stone(props: { color: string; id: number }) {
  const { color, id } = props;

  return <span className={`stone ${color}`}>{id > 0 ? id : ""}</span>;
}
