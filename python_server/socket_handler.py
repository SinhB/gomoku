from .app import app

@app.sio.on('createNewRoom')
async def handle_join(roomName):
    print("JOINED ROOM")
    print(roomName)
    # await app.sio.emit('lobby', 'User joined')