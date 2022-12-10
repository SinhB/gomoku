<script setup>
/* eslint-disable */
import axios from 'axios'
import io from "socket.io-client"
import { reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import PlayerInfos from './PlayerInfos.vue'
import GoStone from './GoStone.vue'

import { useBoardStore } from '../plugins/store/board.ts'

// const address = "127.0.0.1"
const address = "10.12.10.7"

const boardStore = useBoardStore()
const route = useRoute()

// SOCKET MANAGEMENT
const socket = io(`http://${address}:3000`)
// const socket = io("http://localhost:3000")

// PLAYER CONNECTION AND COLOR
const env = reactive({
  myColor: 'spectator',
  availableColor: [],
  mySocketId: ''
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
  socket.on("connect", () => {
    env.mySocketId = socket.id
  })

  socket.on("getBoard", (data) => {
    boardStore.board = data
  })

  socket.on("getAvailableColors", data => {
    env.availableColor = data
    if (env.availableColor.includes('white')) {
    // if (env.availableColor.contains('white')) {
      boardStore.isAI['white'] = true
    }
    if (env.availableColor.includes('black')) {
    // if (env.availableColor.contains('black')) {
      boardStore.isAI['black'] = true
    }
  })
  socket.on("whitePlayer", data => {
    updatePlayer(data, 'white')
  })
  socket.on("blackPlayer", data => {
    updatePlayer(data, 'black')
  })

  // BOARD ACTION
  socket.on("receivePlaceStone", data => {
    performMove(data)
  })
  socket.on("receiveRemoveStone", eatenPos => {
    boardStore.removeStone(eatenPos[0], eatenPos[1])
  })
  socket.on('reset', () => {
    init()
  })

  socket.emit("joinedRoom", route.params.roomName)
})

// BOARD MANAGEMENT

async function getNextMove () {
  const myParams = {
    player: boardStore.player.toString(),
    depth: boardStore.getDepth(),
    board: boardStore.board,
    turn: boardStore.turnsCounter
  }
  const result = await axios.get(`http://${address}:5000/get_best_move?player=${boardStore.player.toString()}&depth=${boardStore.getDepth()}&room=${route.params.roomName}`)
  // const result = await axios.get(`http://${address}:5000/get_best_move?params=${JSON.stringify(myParams)}`)
  if (result.status == 200) {
    boardStore.timer = result.data.timer.toFixed(5)
    await performMove(result.data.best_move)
  }
}

async function selectMove(move) {
  if (boardStore.playerString === env.myColor) {
    socket.emit("placeStone", {room: route.params.roomName, move: move, player: boardStore.player})
  }
}

async function performMove(move) {
  const result = await axios.get(`http://${address}:5000/apply_move?player=${boardStore.player.toString()}&move=${move}&room=${route.params.roomName}`)
  if (result.status === 200) {
    const eatenPos = JSON.parse(result.data.eaten_pos)
    for (const pos in eatenPos['eaten_pos']) {
      socket.emit("removeStone", {room: route.params.roomName, move: eatenPos['eaten_pos'][pos]})
    }

    boardStore.placeStone(move[0], move[1])
    boardStore.updateTotalEat(result.data.total_eat)

    if (boardStore.playerString === env.myColor) {
      socket.emit('updateBoard', {roomName: route.params.roomName, board: boardStore.board})
    }

    console.log(boardStore.autoplay, boardStore.isAI[boardStore.playerString])
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

async function reset () {
  await axios.get(`http://${address}:5000/init?room=${route.params.roomName}`)
  socket.emit('reset', route.params.roomName)
}

async function init () {
  boardStore.$reset()
}

init()

</script>

<template>
  <v-container>
    {{env.availableColor}}
    <h3 :class="`autoplay-switch ${env.myColor}--text`">You are playing {{env.myColor}} -- {{boardStore.playerString}}</h3>

    <br />
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
          <v-btn class="bg-black" @click="reset()">Restart</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <br />

    <v-row>
      <v-col>
        <PlayerInfos color="black" :socket="socket" :availableColor="env.availableColor"/>
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
        <PlayerInfos color="white" :socket="socket" :availableColor="env.availableColor"/>
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
