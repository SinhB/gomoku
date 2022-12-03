<script setup>
/* eslint-disable */
import { useBoardStore } from '../plugins/store/board.ts'

const boardStore = useBoardStore()

const props = defineProps(['color'])

function lowerCase (word) {
  return word.charAt(0) + word.substring(1).toLowerCase()
}
</script>

<template>
  <h1>{{lowerCase(props.color)}} player {{(boardStore.winner === props.color ? 'WIN' : '')}}</h1>
  Total eat : {{boardStore.totalEat[props.color]}}
  <v-switch
    v-model="boardStore.isAI[props.color]"
    :label="boardStore.isAI[props.color] === true ? 'AI': 'PLAYER'"
    @click="(boardStore.isAI[props.color] =  !boardStore.isAI[props.color])"
    color="red"
    class="switch-center"
  ></v-switch>
</template>

<style scoper>
.switch-center {
  display: flex;
  justify-content: center;
}
</style>