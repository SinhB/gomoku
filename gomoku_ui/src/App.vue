<script setup>
// import BoardTest from './components/BoardTest.vue'
// import RoomSelect from './components/RoomSelect.vue'
import appHeader from './components/AppHeader.vue'
import { useBoardStore } from './plugins/store/board.ts'

const boardStore = useBoardStore()
</script>

<template>
  <v-app class="app">

    <appHeader></appHeader>
    <!-- <RoomSelect /> -->
    <!-- <BoardTest /> -->
    <router-view />
    <div class="d-flex justify-center ma-4">
      <v-col sm="6">
        <v-alert dismissible :color="boardStore.alertColor" v-model="boardStore.alert">{{boardStore.alertText}}</v-alert>
      </v-col>
    </div>
  </v-app>
</template>

<style>
.app {
  text-align: center;
  margin-top: 60px;
}
</style>
