
<script setup>
/* eslint-disable */
import { useBoardStore } from '../plugins/store/board.ts';

const boardStore = useBoardStore()

const props = defineProps({
  "player": Number,
  "position": Object
})
</script>

<template>
  <span v-if="props.player === 1" class='stone black'>{{boardStore.board[position.rowIndex][position.colIndex].turn}}</span>
  <span v-if="(props.player === -1)" class='stone white'>{{boardStore.board[position.rowIndex][position.colIndex].turn}}</span>
</template>

<style scoped lang="scss">
.stone {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.7rem;
  &.black {
    background-color: #000;
    color: #fff;
  }
  &.white {
    background-color: #fff;
    color: #000;
    border: 1px solid #000;
  }
}
</style>