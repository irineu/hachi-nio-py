import asyncio
import ssl
import logging

log = logging.getLogger(__name__)

from hachi_nio import HachiNIOClient

def on_connect(ref):
    print("New Connection! " + str(ref.id))
    ref.send({"test" : "123"}, "hello")


def on_data(header, message, ref):
    print(header, ref.id, message.decode("utf-8"))
    # ref.send(header, "hi")

def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    if name := context.get("future").get_coro().__name__ == "on_connected":
        if type(msg) == ZeroDivisionError:
            log.error(f"Caught ZeroDivisionError from on_connected: {msg}")
            return
        log.info(f"Caught another minor exception from on_connected: {msg}")
    else:
        log.error(f"Caught exception from {name}: {msg}")

async def run_client(addr,port):
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.options |= ssl.OP_NO_TLSv1
    ssl_ctx.options |= ssl.OP_NO_TLSv1_1
    # ssl_ctx.load_cert_chain('server-crt.pem', keyfile='server-key.pem')
    # ssl_ctx.load_verify_locations(cafile='ca-crt.pem')
    ssl_ctx.check_hostname = False

    #ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
    ssl_ctx.verify_mode = ssl.VerifyMode.CERT_NONE

    ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_exception)

    transport, protocol = await loop.create_connection(
        lambda: HachiNIOClient(on_data, on_connect),
        addr, port, ssl=ssl_ctx)

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(run_client("0.0.0.0", 7890))
