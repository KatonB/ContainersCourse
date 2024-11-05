import uuid
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()
rooms: Dict[str, List[WebSocket]] = {}


@app.websocket("/chat/{chat_name}")
async def chat_room(websocket: WebSocket, chat_name: str):
    username = f"user_{uuid.uuid4().hex[:8]}"
    await websocket.accept()

    if chat_name not in rooms:
        rooms[chat_name] = []
        print(f"Чат {chat_name} создан")
        print(f"Теперь чаты: {list(rooms.keys())}")
    rooms[chat_name].append(websocket)

    await broadcast(f"{username} присоединился к чату", chat_name)

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
                if message_data.get("type") == "ping":
                    print(f"Получили пинг от {username}")
                    continue
            except json.JSONDecodeError:
                pass

            message = f"{username} :: {data}"
            print(f"Получено сообщение: {message}")
            await broadcast(message, chat_name)
    except WebSocketDisconnect:
        rooms[chat_name].remove(websocket)
        print(f"{username} отключился")
        await broadcast(f"{username} покинул чат", chat_name)

        if not rooms[chat_name]:
            print(f"В комнате {chat_name} никого. Удаляем")
            del rooms[chat_name]


async def broadcast(message: str, chat_name: str):
    for connection in rooms.get(chat_name, []):
        print(f"Бродкастим клиенту {connection} сообщение \"{message}\"")
        await connection.send_text(message)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, ws_ping_interval=600)
