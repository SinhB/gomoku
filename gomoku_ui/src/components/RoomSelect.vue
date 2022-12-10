<script setup>
/* eslint-disable */
import io from "socket.io-client"
import { ref, reactive } from 'vue'

const socket = io("http://localhost:3000")
// const socket = io("http://172.23.163.242:3000")

let rooms = ref([])
let newRoomName = ref('')
socket.on("getRooms", data => {
    rooms.value = data
})

function createNewRoom () {
    console.log("Creating new room")
    socket.emit('createNewRoom', newRoomName.value)
}
</script>

<template>
    <v-row>
        <v-col>
        <form>
            <v-text-field
                v-model="newRoomName"
                label="New room name"
                required
            ></v-text-field>
            <v-btn @click="createNewRoom()" :to="`/game/${newRoomName}`">
                Create a new room
            </v-btn>
        </form>
        </v-col>
        <v-col>
            <v-row v-for="(roomData, roomName) in rooms" :key="roomName">
                <v-btn :to="`/game/${roomName}`">
                    {{roomName}}
                </v-btn>
                <br />
            </v-row>
        </v-col>
    </v-row>
</template>

<style scoped>
</style>
