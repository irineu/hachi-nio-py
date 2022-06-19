import asyncio
from hachi_nio import HachiNIOClient

def on_connect(ref):
    print("New Connection! " + str(ref.id))
    ref.send({"test" : "123"}, "hello")


def on_data(header, message, ref):
    print(header, ref.id, message.decode("utf-8"))
    # ref.send(header, "hi")


async def run_client(addr,port):
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_connection(
        lambda: HachiNIOClient(on_data, on_connect),
        addr, port)

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(run_client("0.0.0.0", 7890))
