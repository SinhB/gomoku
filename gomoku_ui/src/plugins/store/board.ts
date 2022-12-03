import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', {
    state: () => ({
        board: [...Array(19)].map(e => Array(19).fill(0)),
        player: 1,
        timer: 0,
        winner: 0,
        totalEat: {'BLACK': 0, 'WHITE': 0}
    }),
    actions: {
        swapPlayer () {
            this.player = this.player * -1
        },
        placeStone (rowIndex, colIndex) {
            console.log(`row : ${rowIndex}, col : ${colIndex}, player : ${this.player}`)
            this.board[rowIndex][colIndex] = this.player
            this.swapPlayer()
        },
        removeStone (rowIndex, colIndex) {
            this.board[rowIndex][colIndex] = 0
        },
        win () {
            this.winner = this.player
        },
        updateTotalEat (totalEat) {
            this.totalEat['BLACK'] = totalEat['BLACK']
            this.totalEat['WHITE'] = totalEat['WHITE']
        }
    }
})