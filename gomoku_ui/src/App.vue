<script setup>
import BoardTest from './components/BoardTest.vue'
import appHeader from './components/AppHeader.vue'
</script>

<template>
  <v-app class="app">
    <appHeader></appHeader>
    <BoardTest />
  </v-app>
</template>

<style>
.app {
  text-align: center;
  margin-top: 60px;
}
</style>
