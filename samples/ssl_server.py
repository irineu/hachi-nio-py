import asyncio
import ssl
import logging
from hachi_nio import HachiNIOServer

log = logging.getLogger(__name__)


def on_connect(ref):
    print("New Connection! " + str(ref.id))


def on_data(header, message, ref):
    print(header, ref.id, message.decode("utf-8"))
    ref.send(header, "hi")


def handle_exception(loop, context):
    print("xxx")
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    if name := context.get("future").get_coro().__name__ == "on_connected":
        if type(msg) == ZeroDivisionError:
            log.error(f"Caught ZeroDivisionError from on_connected: {msg}")
            return
        log.info(f"Caught another minor exception from on_connected: {msg}")
    else:
        log.error(f"Caught exception from {name}: {msg}")


async def run_server(port):
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_ctx.options |= ssl.OP_NO_TLSv1
    ssl_ctx.options |= ssl.OP_NO_TLSv1_1
    ssl_ctx.options |= ssl.OP_SINGLE_DH_USE
    ssl_ctx.options |= ssl.OP_SINGLE_ECDH_USE
    ssl_ctx.load_cert_chain('server-crt.pem', keyfile='server-key.pem')
    #ssl_ctx.load_verify_locations(cafile='ca-crt.pem')
    ssl_ctx.check_hostname = False

    #ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
    ssl_ctx.verify_mode = ssl.VerifyMode.CERT_NONE

    ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_exception)

    server = await loop.create_server(
        lambda: HachiNIOServer(on_data, on_connect),
        '0.0.0.0', port, ssl=ssl_ctx)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server(7890))
