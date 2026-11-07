import asyncio
import json
from datetime import datetime


class NameServer:
    def init(self, host, port):
        self.host = host
        self.port = port
        self.dizionario = {"time": ("127.0.0.1", 6001), "echo": ("127.0.0.1", 6002)}

    async def server(self, reader, writer):
        pass

    async def avvia(self):
        pass


class TimeServer:
    def init(self, host, port):
        self.host = host
        self.port = port

    async def server(self, reader, writer):
        pass

    async def avvia(self):
        pass


class EchoServer:
    def init(self, host, port):
        self.host = host
        self.port = port

    async def server(self, reader, writer):
        pass

    async def avvia(self):
        pass


async def main():
    name = NameServer("127.0.0.1", 6000)
    time = TimeServer("127.0.0.1", 6001)
    echo = EchoServer("127.0.0.1", 6002)

    await asyncio.gather(
        name.avvia(),
        time.avvia(),
        echo.avvia()

    )


if __name__ == "__main__":
    asyncio.run(main())  # perchè ora main è una funzione asincrona, quindi dobbiamo farlo partire in questo modo
