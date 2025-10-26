# simple_async_http
import asyncio

async def handle_client(reader, writer):
    data = await reader.read(1024)
    lines = data.decode().splitlines()
    if lines: 
        request_line = lines[0]
        print(f"Request: {request_line}")

    responce_body = b"Hi, it is async handling."
    responce = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        + f"Content-Length: {len(responce_body)}\r\n\r\n".encode()
        + responce_body
    )
    writer.write(responce)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    f = handle_client
    a = "127.0.0.1"
    p = "8080"
    server = await asyncio.start_server(f,a,p)

    addr = server.sockets[0].getsockname()
    print(f"Serving async on http://{addr[0]}:{addr[1]}")
    async with server:
        await server.serve_forever()


asyncio.run(main())





