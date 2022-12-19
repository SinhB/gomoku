<script setup>
/* eslint-disable */
import { useBoardStore } from '../plugins/store/board.ts'
import { useRoute } from 'vue-router'

const route = useRoute()

const boardStore = useBoardStore()

const props = defineProps(['color', 'socket', 'availableColor', 'myColor'])

function upperCase (word) {
  return word.charAt(0).toUpperCase() + word.substring(1)
}

function play () {
  props.socket.emit('selectColor', {roomName: route.params.roomName, color: props.color})
}

function quit () {
  props.socket.emit('quit', {room: route.params.roomName, color: props.myColor, disconnect: false} )
}
</script>

<template>
  <v-card class="player-card" :color="props.color">
    <div class="player-card-general">
      <h1>{{upperCase(props.color)}} player {{(boardStore.winner === props.color ? 'WIN' : '')}}</h1>
      <h2>Total eaten: {{boardStore.totalEat[props.color]}}</h2>
    </div>
    <div class="player-card-ai">
      <hr/>
      <v-card-actions v-if="availableColor.includes(color)">
        <v-switch
          v-model="boardStore.isQuickPlay[props.color]"
          label="Quick play"
          @click="(boardStore.isQuickPlay[props.color] = !boardStore.isQuickPlay[props.color])"
          color="green lighten-1"
        ></v-switch>
        <v-slider
          v-model="boardStore.aiDepth[props.color]"
          color="green lighten-1"
          :thumb-color="props.color === 'black' ? 'white' : 'black'"
          :label="`AI depth (${boardStore.aiDepth[props.color]})`"
          show-ticks="always"
          :max="20"
          :min="1"
          :step="1"
        ></v-slider>
        <v-slider
          v-model="boardStore.aiCutoff[props.color]"
          color="green lighten-1"
          :thumb-color="props.color === 'black' ? 'white' : 'black'"
          :label="`AI cutoff percentage : (${boardStore.aiCutoff[props.color] * 10})%`"
          show-ticks="always"
          :max="10"
          :min="0"
          :step="1"
        ></v-slider>
      </v-card-actions>

      <v-btn v-if="props.availableColor.length !== 0 && props.availableColor.includes(props.color) && props.myColor === 'spectator'" @click="play()" class="play-button">
          Play
      </v-btn>
      
      <v-btn v-if="props.myColor === props.color" @click="quit()" class="play-button">
          Quit
      </v-btn>
    </div>
  </v-card>
</template>

<style scoped>
.player-card {
  padding: 10px 10px 0 10px;
}
.player-card-general {
  margin-bottom: 10px;
}
.play-button {
  border-style: solid;
  border-color: green;
  border-width: 3px;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>