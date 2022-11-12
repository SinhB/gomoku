import axios from "axios";
import { IGameCreation } from "../types/general";

export const startGame = async (params: IGameCreation) => {
  let response = await axios.post("http://localhost:8000/game/start", params);
  return response;
};
