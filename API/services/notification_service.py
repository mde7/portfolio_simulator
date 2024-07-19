from typing import Dict
from fastapi import WebSocket

class NotificationService():
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
    
    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
    
    async def send_personal_message(self, message: str, username: str):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            connection.send_text(message)