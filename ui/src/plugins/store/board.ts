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
        aiDepth: { black: 6, white: 6 },
        turns: [...Array(19)].map((e) => Array(19).fill(0)),
        turnsCounter: 0,
        alert: false,
        alertText: '',
        alertColor: ''
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
            this.board[rowIndex][colIndex] = { player: 0, turn: 0 };
        },
        win(player) {
            this.winner = player;
            this.fireAlert(`${player.toUpperCase()} PLAYER HAS WON THE GAME`, 'green')
        },
        updateTotalEat(totalEat) {
            this.totalEat["black"] = totalEat["black"];
            this.totalEat["white"] = totalEat["white"];
        },
        getDepth() {
            if (this.turnsCounter === 1) {
                return 1
            }
            return this.aiDepth[this.playerString];
        },
        async fireAlert(text, color) {
            this.alertColor = color
            this.alertText = text
            this.alert = true
            await new Promise(resolve => setTimeout(resolve, 5000));
            this.alert = false
            this.alertText = ''
            this.alertColor = ''
        },
        reset() {
            this.board = [...Array(19)].map((e) => Array(19).fill({ player: 0, turn: 0 }))
            this.player = 1
            this.playerString = "black"
            this.timer = "0.00000"
            this.winner = ""
            this.totalEat = { black: 0, white: 0 }
            this.turns = [...Array(19)].map((e) => Array(19).fill(0))
            this.turnsCounter = 0
        }
    },
});