import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', {
    state: () => ({
        board: [...Array(19)].map(e => Array(19).fill(0)),
        player: 1,
        playerString: 'black',
        timer: "0.00000",
        winner: '',
        totalEat: {'black': 0, 'white': 0},
        isAI: {'black': false, "white": false},
        autoplay: false,
        aiDepth: {'black': 10, "white": 10},
    }),
    actions: {
        swapPlayer () {
            this.player = this.player * -1
            this.playerString = this.playerString === 'black' ? 'white' : 'black'
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
            this.totalEat['black'] = totalEat['black']
            this.totalEat['white'] = totalEat['white']
        },
        getDepth () {
            return this.aiDepth[this.playerString]
        }
    }
})