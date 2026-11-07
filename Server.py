import asyncio
import json
from datetime import datetime


class NameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dizionario = {"time": ("127.0.0.1", 6001), "echo": ("127.0.0.1", 6002)}

    async def server(self, reader, writer):
        addr = writer.get_extra_info("peername")
        print(f"Client {addr[0]} , {addr[1]} connesso a name server")
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                richiesta_json = json.loads(data.decode())
                if richiesta_json["service"] == "time":
                    diz_risposta = {
                        "status": "ok",
                        "service": "time",
                        "host": self.dizionario["time"][0],
                        "port": self.dizionario["time"][1]
                    }
                    risposta_json = json.dumps(diz_risposta) + "\n"
                    writer.write(risposta_json.encode())
                await writer.drain()
        except Exception as e:
            print(f"Errore {e}")
        finally:
            if writer:
                writer.close()
                await writer.wait_closed()
            print(f"Chiusura della connessione al client {addr[0]} , {addr[1]}")

    async def avvia(self):
        s = await asyncio.start_server(self.server, self.host, self.port)
        async with s:
            await s.serve_forever()


class TimeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def server(self, reader, writer):
        try:
            addr = writer.get_extra_info("peername")
            print(f"Client {addr[0]} , {addr[1]} connesso a time server")
            while True:

                data = await reader.readline()
                if not data:
                    break
                data_json = json.loads(data.decode())
                if data_json["cmd"] != "time":
                    print("Comando errato")
                    break
                data_ora = datetime.now()
                data_ora_formattate = data_ora.strftime("%Y-%m-%d %H:%M:%S")
                diz_risp = {
                    "status": "ok",
                    "time": data_ora_formattate
                }
                risposta = json.dumps(diz_risp) + "\n"
                writer.write(risposta.encode())
                await writer.drain()
        except KeyboardInterrupt:
            print("Interruzione da tastiera")
        except Exception as e:
            print(f"Errore {e}")
        finally:
            if writer:
                writer.close()
                await writer.wait_closed()
            print(f"Connessione Time Server con client {addr[0]} , {addr[1]} terminata")

    async def avvia(self):
        s = await asyncio.start_server(self.server, self.host, self.port)
        async with s:
            await s.serve_forever()


class EchoServer:
    def __init__(self, host, port):
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
