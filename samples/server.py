import asyncio
from hachi_nio import HachiNIOServer


def on_connect(ref):
    print("New Connection! " + str(ref.id))


def on_data(header, message, ref):
    print(header, ref.id, message.decode("utf-8"))
    ref.send(header, "hi")


async def run_server(port):
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: HachiNIOServer(on_data, on_connect),
        '0.0.0.0', port)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server(7890))
