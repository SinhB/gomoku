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
        rooms[data.room][data.color] = null
        if (data.disconnect === true) {
            socket.leave(data.room)
        } else {
            socket.emit("spectate")
        }
        delete players[socket.id]
        SocketIo.to(data.room).emit('getAvailableColors', getAvailableColors(data.room))
    })

    socket.on('joinedRoom', roomName => {
        socket.join(roomName)
        socket.emit('color', 'spectator')
        socket.emit('getAvailableColors', getAvailableColors(roomName))
        socket.emit('getBoard', rooms[roomName].board)
    })

    socket.on("createNewRoom", roomName => {
        rooms[roomName] = {white: null, black: null, moves: []}
        rooms[roomName] = {white: null, black: null, board: [...Array(19)].map(e => Array(19).fill(0))}
        SocketIo.emit("getRooms", rooms)
    })

    socket.on("updateBoard", data => {
        rooms[data.roomName].board = data.board
    })

    socket.on("placeStone", data => {
        SocketIo.to(data.room).emit("receivePlaceStone", data.move)
    })

    socket.on("removeStone", data => {
        SocketIo.to(data.room).emit("receiveRemoveStone", data.move)
    })

    socket.on("reset", (roomName) => {
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