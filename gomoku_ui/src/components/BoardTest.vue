<script setup>
/* eslint-disable */
import axios from 'axios'
import { reactive, ref } from 'vue'

let player = ref(1)
let bestMove = []
let timer = 0
let board = reactive({board: [...Array(19)].map(e => Array(19).fill(0))})

async function getNextMove () {
  const result = await axios.get(`http://127.0.0.1:5000/get_best_move?player=${player.value.toString()}`)
  if (result.status == '200') {
    bestMove = result.data.best_move
    timer = result.data.timer
  }
  console.log(bestMove)
  console.log(timer)
  console.log(board)
  await performMove(bestMove)
}

async function performMove(move) {
  const result = await axios.get(`http://127.0.0.1:5000/apply_move?player=${player.value.toString()}&move=${move}`)
  console.log(result)

  board.board[move[0]][move[1]] = player.value

  player.value = player.value * -1
  console.log(player)
}

async function init () {
  const result = await axios.get(`http://127.0.0.1:5000/init`)
}

init()

</script>

<template>
  <v-btn @click="getNextMove()">Get next move</v-btn>
  <!-- {{board.board}}
  {{player}} -->
  <div>
    <v-row v-for="row in board.board" :key="row">
      <v-col v-for="col in row" :key="col">
        <!-- <img :src="getTile(row,col)" class="tileImage"> -->
        <div>{{row[col]}}</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col align="center">
        <h3>Player {{player}} turn</h3>
      </v-col>
    </v-row>
  </div>
</template>


<style scoped>

</style>
