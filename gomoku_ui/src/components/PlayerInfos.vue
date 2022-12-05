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
  <v-card class="player-card" :color="props.color" elevation="24">
    <h1>{{upperCase(props.color)}} player {{(boardStore.winner === props.color ? 'WIN' : '')}}</h1>
    
    <h2>Total eat : {{boardStore.totalEat[props.color]}}</h2>

    <v-card-actions>
      <v-switch
        v-model="boardStore.isAI[props.color]"
        label="AI"
        @click="(boardStore.isAI[props.color] =  !boardStore.isAI[props.color])"
        color="red"
      ></v-switch>
      <v-slider
        v-model="boardStore.aiDepth[props.color]"
        color="red"
        :thumb-color="props.color === 'black' ? 'white' : 'black'"
        :label="`AI depth (${boardStore.aiDepth[props.color]})`"
        show-ticks="always"
        :max="20"
        :min="1"
        :step="1"
      ></v-slider>
    </v-card-actions>

  </v-card>
</template>

<style scoped>
.player-card {
  border: solid 10px #7C90DB;
}
</style>