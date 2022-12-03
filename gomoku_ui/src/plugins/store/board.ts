import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', {
    state: () => ({
        board: [...Array(19)].map(e => Array(19).fill(0)),
        player: 1,
        playerString: 'BLACK',
        timer: 0,
        winner: '',
        totalEat: {'BLACK': 0, 'WHITE': 0},
        isAI: {'BLACK': false, "WHITE": false},
        autoplay: false
    }),
    actions: {
        swapPlayer () {
            this.player = this.player * -1
            this.playerString = this.playerString === 'BLACK' ? 'WHITE' : 'BLACK'
        },
        placeStone (rowIndex, colIndex) {
            this.board[rowIndex][colIndex] = this.player
        },
        removeStone (rowIndex, colIndex) {
            this.board[rowIndex][colIndex] = 0
        },
        win () {
            this.winner = this.playerString
        },
        updateTotalEat (totalEat) {
            this.totalEat['BLACK'] = totalEat['BLACK']
            this.totalEat['WHITE'] = totalEat['WHITE']
        }
    }
})