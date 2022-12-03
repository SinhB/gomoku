<script setup>
/* eslint-disable */
import axios from 'axios'
import PlayerInfos from './PlayerInfos.vue'

import { useBoardStore } from '../plugins/store/board.ts'

const boardStore = useBoardStore()

let bestMove = []

async function getNextMove () {
  const result = await axios.get(`http://127.0.0.1:5000/get_best_move?player=${boardStore.player.toString()}`)
  if (result.status == '200') {
    bestMove = result.data.best_move
    boardStore.timer = result.data.timer
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
  <v-container mt-5>
    <v-btn class="bg-brown" @click="getNextMove()">Get next move</v-btn>
    <v-btn class="bg-brown" @click="init()">Restart</v-btn>
    <v-switch
        v-model="boardStore.autoplay"
        :label="boardStore.autoplay === true ? 'Autoplay enabled': 'Autoplay disabled'"
        @click="(boardStore.autoplay =  !boardStore.autoplay)"
        color="red"
        class="switch-center"
    ></v-switch>
    <p>Last timer : {{boardStore.timer}}</p>
    <br/>
    <br/>
    
    <v-row>
      <v-col>
        <PlayerInfos color="BLACK"/>
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
        <PlayerInfos color="WHITE"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.switch-center {
  display: flex;
  justify-content: center;
}
.board {
  height: 660px;
  width: 760px;
  background-color: bisque;
  margin-left: auto;
  margin-right: auto;
  border: 1px black solid;
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
  margin-top: auto;
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
