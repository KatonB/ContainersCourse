import asyncio
import websockets


async def chat_window(chat_name: str):
    uri = f"ws://127.0.0.1:8080/chat/{chat_name}"
    async with websockets.connect(uri) as websocket:
        print(f"Окно чата для комнаты: {chat_name}")
        print("Ожидание сообщений...")

        while True:
            try:
                message = await websocket.recv()
                print(message)
            except websockets.ConnectionClosed:
                print("Отключен от чата.")
                break


if __name__ == "__main__":
    chat_name = input("Введите название комнаты: ")
    asyncio.run(chat_window(chat_name))
