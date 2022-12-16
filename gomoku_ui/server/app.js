const Express = require("express")()
const Http = require('http').Server(Express)
const SocketIo = require("socket.io")(Http, {
    cors: {
        origin: '*',
        methods: ["GET", "POST"]
    }
})

var players = {}

var rooms = {}

function getAvailableColors(roomName) {
    let availableColors = []
    for (const key in rooms[roomName]) {
        if (rooms[roomName][key] === null) {
            availableColors.push(key)
        }
    }
    return availableColors
}

SocketIo.on("connect", socket => {
    socket.send(socket.id)
    socket.emit("getRooms", rooms)

    socket.on('selectColor', data => {
        rooms[data.roomName][data.color] = socket.id
        players[socket.id] = {roomName: data.roomName, color: data.color}
        console.log(`Emiting ${data.color}Player`)
        SocketIo.to(data.roomName).emit(`${data.color}Player`, socket.id)
    })

    socket.on('quit', data => {
        if (data.room in rooms) {
            rooms[data.room][data.color] = null
            if (data.disconnect === true) {
                socket.leave(data.room)
            } else {
                socket.emit("spectate")
            }
            delete players[socket.id]
            SocketIo.to(data.room).emit('getAvailableColors', getAvailableColors(data.room))    
        }
    })

    socket.on('joinedRoom', roomName => {
        socket.join(roomName)
        socket.emit('roomData', rooms[roomName])
        socket.emit('getAvailableColors', getAvailableColors(roomName))
    })

    socket.on("createNewRoom", roomName => {
        rooms[roomName] = {
            white: null,
            black: null,
            board: [...Array(19)].map(e => Array(19).fill({ player: 0, turn: 0 })),
            playerTurn: 1,
            turnsCounter: 0,
            autoplay: true,
            hardMode: false
        }
        SocketIo.emit("getRooms", rooms)
    })

    socket.on("switchAutoplay", room => {
        rooms[room].autoplay = !rooms[room].autoplay
        SocketIo.to(room).emit("autoplay", rooms[room].autoplay)
    })

    socket.on("switchHardMode", room => {
        rooms[room].hardMode = !rooms[room].hardMode
        SocketIo.to(room).emit("hardMode", rooms[room].hardMode)
    })

    socket.on('win', data => {
        SocketIo.to(data.room).emit("gameOver", data.winner)
    })

    socket.on('eat', data => {
        SocketIo.to(data.room).emit("updateEat", data.total_eat)
    })

    socket.on("placeFreeStone", data => {
        rooms[data.room].turnsCounter += 1
        rooms[data.room].board[data.move[0]][data.move[1]] = {player: rooms[data.room].playerTurn, turn: rooms[data.room].turnsCounter}
        rooms[data.room].playerTurn = rooms[data.room].playerTurn * -1
        SocketIo.to(data.room).emit("receivePlaceFreeStone", data.move)
    })

    socket.on("placeStone", data => {
        rooms[data.room].turnsCounter += 1
        rooms[data.room].board[data.move[0]][data.move[1]] = {player: rooms[data.room].playerTurn, turn: rooms[data.room].turnsCounter}
        rooms[data.room].playerTurn = rooms[data.room].playerTurn * -1
        SocketIo.to(data.room).emit("receivePlaceStone", data.move)
    })

    socket.on("removeStone", data => {
        rooms[data.room].board[data.move[0]][data.move[1]] = {player: 0, turn: 0}
        SocketIo.to(data.room).emit("receiveRemoveStone", data.move)
    })

    socket.on("reset", (roomName) => {
        rooms[roomName].playerTurn = 1
        rooms[roomName].turnsCounter = 0
        rooms[roomName].board = [...Array(19)].map(e => Array(19).fill({ player: 0, turn: 0 }))
        SocketIo.to(roomName).emit("reset")
    })

    socket.on("disconnect", () => {
        console.log("Disconnect")
        if (socket.id in Object.keys(players)) {
            SocketIo.to(players[socket.id].roomName).emit('getAvailableColors', getAvailableColors(players[socket.id].roomName))
            rooms[players[socket.id].roomName][players[socket.id].color] = null
            delete players[socket.id]
        }
    })
})

const address = require('../../network.json').address
Http.listen(3000, address, () => {
// Http.listen(3000, () => {
    console.log("Listening on port 3000")
})