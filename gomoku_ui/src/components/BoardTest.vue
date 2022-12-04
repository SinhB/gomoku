<script setup>
/* eslint-disable */
import axios from 'axios'
import PlayerInfos from './PlayerInfos.vue'

import { useBoardStore } from '../plugins/store/board.ts'

const boardStore = useBoardStore()

let bestMove = []

async function getNextMove () {
  const result = await axios.get(`http://127.0.0.1:5000/get_best_move?player=${boardStore.player.toString()}&depth=${boardStore.getDepth()}`)
  if (result.status == '200') {
    bestMove = result.data.best_move
    boardStore.timer = result.data.timer.toFixed(5)
  }
  await performMove(bestMove)
}

async function performMove(move) {
  const result = await axios.get(`http://127.0.0.1:5000/apply_move?player=${boardStore.player.toString()}&move=${move}`)
  if (result.status === 200) {
    const eatenPos = JSON.parse(result.data.eaten_pos)
    for (const pos in eatenPos['eaten_pos']) {
      boardStore.removeStone(eatenPos['eaten_pos'][pos][0], eatenPos['eaten_pos'][pos][1])
    }

    
    boardStore.placeStone(move[0], move[1])

    boardStore.updateTotalEat(result.data.total_eat)

    if (result.data.win === true) {
      boardStore.win()
      print("WIN")
    } else {
      boardStore.swapPlayer()
      if (boardStore.autoplay && boardStore.isAI[boardStore.playerString]) {
        await getNextMove()
      }
    }
  }
}

async function init () {
  await axios.get(`http://127.0.0.1:5000/init`)
  boardStore.$reset()
}

init()

</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-card class="general-card" flat tile elevation="24">
        <v-card-actions>
          <h3 class="autoplay-switch">Last timer : {{boardStore.timer}}</h3>
          <v-switch
            v-model="boardStore.autoplay"
            :label="boardStore.autoplay === true ? 'Autoplay enabled': 'Autoplay disabled'"
            @click="(boardStore.autoplay =  !boardStore.autoplay)"
            color="red"
            class="autoplay-switch"
          ></v-switch>
          <v-btn class="bg-black" @click="getNextMove()">Get next move</v-btn>
          <v-btn class="bg-black" @click="init()">Restart</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <br />

    <v-row>
      <v-col>
        <PlayerInfos color="black"/>
      </v-col>

      <v-col>
        <div class="board">
          <v-row v-for="(row, rowIndex) in boardStore.board" :key="row, rowIndex">
            <v-col class="tile" v-for="(col, colIndex) in row" :key="col, colIndex">
              <img v-if="col === 1" class='stone' src="../assets/black_stone.png">
              <img v-if="col === -1" class='stone' src="../assets/white_stone.png">
              <div v-if="col === 0" class="clickableTile" @click="performMove([rowIndex, colIndex])">
                <img class='emptyTile' src="../assets/black_stone.png">
              </div>
            </v-col>
          </v-row>
        </div>
      </v-col>

      <v-col>
        <PlayerInfos color="white"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.autoplay-switch {
  display: flex;
  justify-content: center;
}
.general-card {
  border: solid 2px black;
  width: 900px;
}
.board {
  height: 663px;
  width: 663px;
  background-color: rgb(228, 163, 133);
  margin-left: auto;
  margin-right: auto;
  border: 3px black solid;
}
.tile {
  height: 48px;
  width: 48px;
  margin: 0;
  padding: 0;
}
.stone {
  height: 20px;
  width: 20px;
  margin-top: 6px;
  margin-bottom: auto;
  margin-left: auto;
  margin-right: auto;
}
.clickableTile {
  cursor: pointer;
  margin-top: auto;
  padding-bottom: 10px;
  margin-left: auto;
  margin-right: auto;
}
.emptyTile {
  cursor: pointer;
  height: 2px;
  width: 2px;
  max-height: 100%;
  max-width: 100%;
  border: 1px black solid;
}
</style>
