import { defineStore } from 'pinia'

export const useBoardStore = defineStore("board", {
    state: () => ({
        board: [...Array(19)].map((e) => Array(19).fill({ player: 0, turn: 0 })),
        player: 1,
        playerString: "black",
        timer: "0.00000",
        winner: "",
        totalEat: { black: 0, white: 0 },
        isAI: { black: true, white: true },
        autoplay: true,
        aiDepth: { black: 10, white: 10 },
        turns: [...Array(19)].map((e) => Array(19).fill(0)),
        turnsCounter: 0,
    }),
    actions: {
        swapPlayer() {
            this.player = this.player * -1;
            this.playerString = this.playerString === "black" ? "white" : "black";
        },
        placeStone(rowIndex, colIndex) {
            this.turnsCounter += 1;
            this.turns[rowIndex][colIndex] = this.turnsCounter;
            this.board[rowIndex][colIndex] = {
                player: this.player,
                turn: this.turnsCounter,
            };
        },
        removeStone(rowIndex, colIndex) {
            this.board[rowIndex][colIndex] = 0;
        },
        win(player) {
            this.winner = player;
        },
        updateTotalEat(totalEat) {
            this.totalEat["black"] = totalEat["black"];
            this.totalEat["white"] = totalEat["white"];
        },
        getDepth() {
            return this.aiDepth[this.playerString];
        },
    },
});