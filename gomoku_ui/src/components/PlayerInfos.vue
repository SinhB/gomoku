<script setup>
/* eslint-disable */
import { useBoardStore } from '../plugins/store/board.ts';

const boardStore = useBoardStore()

const props = defineProps(['color'])

function upperCase (word) {
  return word.charAt(0).toUpperCase() + word.substring(1)
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
      <v-card-actions>
        <v-switch
          v-model="boardStore.isAI[props.color]"
          label="AI"
          @click="(boardStore.isAI[props.color] =  !boardStore.isAI[props.color])"
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
      </v-card-actions>
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
</style>