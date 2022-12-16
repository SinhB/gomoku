<script setup>
/* eslint-disable */
import axios from 'axios'
import io from "socket.io-client"
import { reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'

import PlayerInfos from './PlayerInfos.vue'
import GoStone from './GoStone.vue'

import { useBoardStore } from '../plugins/store/board.ts'

// const address = "127.0.0.1"
const address = require('../../../network.json').address
// const address = "10.12.10.7"

const boardStore = useBoardStore()
const route = useRoute()

// SOCKET MANAGEMENT
const socket = io(`http://${address}:3000`)
// const socket = io("http://localhost:3000")

// PLAYER CONNECTION AND COLOR
const env = reactive({
  myColor: 'spectator',
  availableColor: [],
  mySocketId: '',
  freePlay: 0
})


function updatePlayer (data, color) {
  console.log("Update player")
  if (env.mySocketId === data) {
    env.myColor = color
  }
  boardStore.isAI[color] = false
  env.availableColor = env.availableColor.filter(function(ele){ 
    return ele != color
  })
}

onMounted(() => {
  console.log("INIT")
  init()

  socket.on("connect", () => {
    env.mySocketId = socket.id
  })

  socket.on("roomData", (data) => {
    env.myColor = 'spectator'
    boardStore.board = data.board
    if (boardStore.player !== data.playerTurn) {
      boardStore.swapPlayer()
    }
    boardStore.autoplay = data.autoplay
    boardStore.turnsCounter = data.turnsCounter
  })

  socket.on("getAvailableColors", data => {
    env.availableColor = data
    boardStore.isAI['white'] = env.availableColor.includes('white') ? true : false
    boardStore.isAI['black'] = env.availableColor.includes('black') ? true : false
  })
  socket.on("whitePlayer", data => {
    updatePlayer(data, 'white')
  })
  socket.on("blackPlayer", data => {
    updatePlayer(data, 'black')
  })
  socket.on("spectate", () => {
    env.myColor = 'spectator'
  })

  socket.on('gameOver', player => {
    boardStore.win(player)
  })

  // BOARD ACTION
  socket.on("receivePlaceFreeStone", async (move) => {
    boardStore.placeStone(move[0], move[1])
    boardStore.swapPlayer()
  })
  socket.on("receivePlaceStone", async (move) => {
    boardStore.placeStone(move[0], move[1])
    const currentPlayer = boardStore.playerString
    const currentPlayerIsAI = boardStore.isAI[boardStore.playerString]
    boardStore.swapPlayer()
    if (
      (currentPlayerIsAI || env.myColor === currentPlayer)
      && boardStore.autoplay
      && boardStore.isAI[boardStore.playerString]
      && boardStore.winner === ''
    ) {
      await getNextMove()
    }
  })
  socket.on("receiveRemoveStone", eatenPos => {
    boardStore.removeStone(eatenPos[0], eatenPos[1])
  })
  socket.on('reset', () => {
    init()
  })

  socket.on('autoplay', (autoplay) => {
    boardStore.autoplay = autoplay
  })
  
  socket.on('hardMode', (hardMode) => {
    boardStore.hardMode = hardMode
  })
  socket.on('updateEat', total_eat => {
    boardStore.updateTotalEat(total_eat)
  })

  socket.emit("joinedRoom", route.params.roomName)
})
const currentRoom = route.params.roomName
onBeforeUnmount(() => {
  socket.emit('quit', {room: currentRoom, color: env.myColor, disconnect: true} )
})
// BOARD MANAGEMENT

async function getNextMove () {
  const result = await axios.get(`http://${address}:5000/get_best_move?player=${boardStore.player.toString()}&depth=${boardStore.getDepth()}&room=${route.params.roomName}&hard_mode=${boardStore.hardMode}`)
  if (result.status == 200) {
    boardStore.timer = result.data.timer.toFixed(5)
    await performMove(result.data.best_move)
  }
}

async function selectMove(move) {
  if (boardStore.board[move[0]][move[1]].player === 0 && boardStore.winner === '') {
    if (env.freePlay > 0) {
      const result = await axios.get(`http://${address}:5000/apply_move?player=${boardStore.player.toString()}&move=${move}&room=${route.params.roomName}`)
      if (result.status === 200) {
        if (result.data.forbidden_move === true) {
          boardStore.fireAlert('Forbidden move', 'red')
        } else {
          socket.emit("placeFreeStone", {room: route.params.roomName, move: move, player: boardStore.player})
          env.freePlay -= 1
        }
      }
    } else if (boardStore.playerString === env.myColor) {
      await performMove(move)
    }
  }
}

async function performMove(move) {
  const result = await axios.get(`http://${address}:5000/apply_move?player=${boardStore.player.toString()}&move=${move}&room=${route.params.roomName}`)
  if (result.status === 200) {
    if (result.data.forbidden_move === true) {
      boardStore.fireAlert('Forbidden move', 'red')
    } else {
      const eatenPos = JSON.parse(result.data.eaten_pos)
      for (const pos in eatenPos['eaten_pos']) {
        socket.emit("removeStone", {room: route.params.roomName, move: eatenPos['eaten_pos'][pos]})
      }

      if (result.data.win === true) {
        socket.emit("win", {room: route.params.roomName, winner: boardStore.playerString})
      }
      socket.emit("placeStone", {room: route.params.roomName, move: move, player: boardStore.player})

      socket.emit('eat', {room: route.params.roomName, total_eat: result.data.total_eat})
    }
  }
}

async function createOpeningBoard () {
  env.freePlay = 3
}

async function reset () {
  await axios.get(`http://${address}:5000/init?room=${route.params.roomName}`)
  socket.emit('reset', route.params.roomName)
}

async function init () {
  await boardStore.reset()
}

async function switchAutoplay() {
  socket.emit('switchAutoplay', route.params.roomName)
}

async function switchHardMode() {
  socket.emit('switchHardMode', route.params.roomName)
}
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
            @click="switchAutoplay()"
            color="red"
            class="autoplay-switch"
          ></v-switch>
          <v-switch
            v-model="boardStore.hardMode"
            :label="boardStore.hardMode === true ? 'Hard mode enabled': 'Hard mode disabled'"
            @click="switchHardMode()"
            color="red"
            class="autoplay-switch"
          ></v-switch>
          <v-btn @click="createOpeningBoard()">OPENING</v-btn>
          <v-btn @click="getNextMove()">Get next move</v-btn>
          <v-btn @click="reset()">Restart</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <br />
    
    <v-row justify="center">
      <h3 :class="`player-turn bg-${boardStore.playerString}`">PLAYER TURN</h3>
    </v-row>

    <v-row>
      <v-col>
        <PlayerInfos color="black" :socket="socket" :availableColor="env.availableColor" :myColor="env.myColor" />
      </v-col>

      <v-col>
        <div class="board">
          <div class="container">
            <v-row class="row-content" v-for="(row, rowIndex) in boardStore.board" :key="row, rowIndex">
              <v-col class="square" v-for="(col, colIndex) in row" :key="col, colIndex" @click="selectMove([rowIndex, colIndex])">
                <div class="square-content">
                  <GoStone :player="col.player" :position="{rowIndex: rowIndex, colIndex: colIndex}" />
                </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-col>

      <v-col>
        <PlayerInfos color="white" :socket="socket" :availableColor="env.availableColor" :myColor="env.myColor" />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">
.player-turn {
  display: flex;
  justify-content: center;
  padding-top: 11px;
  width: 600px;
  height: 50px;
  margin-bottom: 20px;
}
.autoplay-switch {
  display: flex;
  justify-content: center;
}
.general-card {
  width: 1200px;
  // margin: 40px 0;
  margin-top: 10px;
  margin-bottom: 20px;
  background-color: #35393C;
}
.tile {
  height: 48px;
  width: 48px;
  margin: 0;
  padding: 0;
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

</style>
