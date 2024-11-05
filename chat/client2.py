import json
import asyncio
import websockets


async def chat_client(chat_name: str):
    uri = f"ws://127.0.0.1:8080/chat/{chat_name}"
    async with websockets.connect(uri) as websocket:
        print(
            f"Подключен к комнате {chat_name}. Введите сообщение и нажмите Enter для отправки. Введите 'exit' для выхода.")

        async def receive():
            while True:
                try:
                    message = await websocket.recv()
                    print(message)
                except websockets.ConnectionClosed:
                    print("Отключен от чата.")
                    break

        receive_task = asyncio.create_task(receive())

        while True:
            message = input()
            if message.lower() == 'exit':
                break
            await websocket.send(message)

        receive_task.cancel()

async def main():
    while True:
        chat_name = input("Введите название комнаты: ")
        await chat_client(chat_name)

if __name__ == "__main__":
    asyncio.run(main())
