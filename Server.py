import asyncio
import json
from datetime import datetime


class NameServer:
    def init(self, host, port):
        self.host = host
        self.port = port
        self.dizionario = {"time": ("127.0.0.1", 6001), "echo": ("127.0.0.1", 6002)}

    async def server(self, reader, writer):
        addr = writer.get_extra_info("peername")
        print(f"Client {addr[0]} , {addr[1]} connesso a name server")
        while True:
            data = await reader.readline()
            if not data:
                break
            richiesta_json = json.loads(data.decode())
            if richiesta_json["service"] == "time":
                diz_risposta = {
                    "status" : "ok",
                    "service" : "time" ,
                    "host" : self.dizionario["time"][0],
                    "port": self.dizionario["time"][1]
                }
                risposta_json = json.dumps(diz_risposta) + "\n"
                writer.write(risposta_json.encode())
            await writer.drain()

    async def avvia(self):
        s = await asyncio.start_server(self.server, self.host, self.port)
        async with s:
            await s.serve_forever()


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
