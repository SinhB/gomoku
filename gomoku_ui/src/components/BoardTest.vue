<script setup>
/* eslint-disable */
import axios from 'axios'
import { useBoardStore } from '../plugins/store/board.ts'

const boardStore = useBoardStore()

let bestMove = []

async function getNextMove () {
  const result = await axios.get(`http://127.0.0.1:5000/get_best_move?player=${boardStore.player.toString()}`)
  if (result.status == '200') {
    bestMove = result.data.best_move
    boardStore.timer = result.data.timer
  }
  console.log(bestMove)
  console.log(boardStore.board)
  await performMove(bestMove)
}

async function performMove(move) {
  const result = await axios.get(`http://127.0.0.1:5000/apply_move?player=${boardStore.player.toString()}&move=${move}`)
  console.log(result)

  boardStore.placeStone(move[0], move[1])
  console.log(boardStore.player)
}

async function init () {
  const result = await axios.get(`http://127.0.0.1:5000/init`)
  boardStore.$reset()
}

function getTile(value) {
  console.log(`value : ${value}`)
  if (value === 1) {
    return '../assets/black_stone.png'
  }
  else if (value === -1) {
    return '../assets/white_stone.png'
  }
  else if (value === 0) {
    return '../assets/logo.png'
  }
}

init()

</script>

<template>
  <v-container mt-5>
    <v-btn class="bg-brown" @click="getNextMove()">Get next move</v-btn>
    <v-btn class="bg-brown" @click="init()">Restart</v-btn>
    <p>Last timer : {{boardStore.timer}}</p>
    <br/>
    <br/>
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
  </v-container>
</template>

<style scoped>
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
