import { IStone } from "../types/general";

export default function Stone(props: IStone) {
  const { color, id } = props;

  return <span className={`stone ${color}`}>{id >= 0 ? id : ""}</span>;
}
