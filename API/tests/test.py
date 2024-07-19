import asyncio
import websockets

async def listen_to_notifications():
    uri = "ws://localhost:8000/notifications/ws/testuser"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(listen_to_notifications())
