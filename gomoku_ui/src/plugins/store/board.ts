import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', {
    state: () => ({
        board: [...Array(19)].map(e => Array(19).fill(0)),
        player: 1,
        timer: 0
    }),
    actions: {
        swapPlayer () {
            this.player = this.player * -1
        },
        placeStone (rowIndex, colIndex) {
            console.log(`row : ${rowIndex}, col : ${colIndex}, player : ${this.player}`)
            this.board[rowIndex][colIndex] = this.player
            this.swapPlayer()
        }
    }
})