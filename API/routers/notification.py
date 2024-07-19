from services.notification_service import NotificationService
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

def get_notification_router(notification_service: NotificationService):
    @router.websocket("/ws/{user}")
    async def websocket_endpoint(websocket: WebSocket, user: str):
        await notification_service.connect(user, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await notification_service.send_personal_message(f"Message text from {user} was: {data}", user)
        except WebSocketDisconnect:
            notification_service.disconnect(user)
            await notification_service.broadcast(f"User {user} left the chat")
    
    return router