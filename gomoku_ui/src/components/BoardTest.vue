<script setup>
/* eslint-disable */
import axios from 'axios';
import GoStone from './GoStone.vue';
import PlayerInfos from './PlayerInfos.vue';

import { useBoardStore } from '../plugins/store/board.ts';

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
      <v-card class="general-card" flat>
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
          <div class="container">
            <v-row class="row-content" v-for="(row, rowIndex) in boardStore.board" :key="row, rowIndex">
              <v-col class="square" v-for="(col, colIndex) in row" :key="col, colIndex" @click="performMove([rowIndex, colIndex])">
                <div class="square-content">
                  <GoStone :player="col.player" :position="{rowIndex: rowIndex, colIndex: colIndex}" />
                </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-col>

      <v-col>
        <PlayerInfos color="white"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">
.autoplay-switch {
  display: flex;
  justify-content: center;
}
.general-card {
  width: 900px;
  margin: 40px 0;
  background-color: #35393C;
}

.tile {
  height: 48px;
  width: 48px;
  margin: 0;
  padding: 0;
}

.board {
  margin: auto;
  height: 600px;
  width: 600px;
  overflow: hidden;
  border: 4px solid #000;
  background-color: #fcf6ec;
}

.container .square {
  display: flex;
  justify-content: center;
  align-items: center;
  aspect-ratio: 1 / 1;
  align-items: center;
  background: linear-gradient(
      to left,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0) calc(50% - 0.8px),
      rgba(0, 0, 0, 1) 50%,
      rgba(0, 0, 0, 0) calc(50% + 0.8px),
      rgba(0, 0, 0, 0) 100%
    ),
    linear-gradient(
      to top,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0) calc(50% - 0.8px),
      rgba(0, 0, 0, 1) 50%,
      rgba(0, 0, 0, 0) calc(50% + 0.8px),
      rgba(0, 0, 0, 0) 100%
    );
}

.square-content {
  position: absolute;
}

.row-content {
  margin: 0;
}

.container .square:hover {
  cursor: pointer;
  background-color: #6b665c;
  border-radius: 100%;
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
