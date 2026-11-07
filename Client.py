import json
import asyncio
import sys


async def connessione_NameServer():
    if len(sys.argv) < 2:
        print("Errore!!! non abbastanza argomenti inseriti. Formattazione corretta: python nome_file.py nome_server")
        return
    server = sys.argv[1]
    addr, port = None, None
    reader, writer = None, None
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1',
                                                       6000)  # per aprire una connessione in modo asincrono
        richiesta_diz = {
            "cmd": "lookup",
            "service": server
        }
        richiesta_json = json.dumps(richiesta_diz) + "\n"

        writer.write(richiesta_json.encode())
        await writer.drain()

        risposta = await reader.readline()
        risposta_json = json.loads(risposta.decode())

        if risposta_json["status"] == "ok":
            addr = risposta_json["host"]
            port = risposta_json["port"]

    except KeyboardInterrupt:
        print("Interruzione da tastiera")
    except Exception as e:
        print(f"Errore!! {e}")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print("Connessione terminata")

    if addr and port:
        await connessione_server(addr, port, server)


async def connessione_server(addr, port, server):
    reader, writer = None, None
    try:
        reader, writer = await asyncio.open_connection(addr, port)  # per aprire una connessione in modo asincrono
        print("Connesso al secondo server")
        if server == "time":
            richiesta_diz = {
                "cmd": "time"
            }
            richiesta_json = json.dumps(richiesta_diz) + "\n"
            writer.write(richiesta_json.encode())
            await writer.drain()

            risposta = await reader.readline()
            risposta_json = json.loads(risposta.decode())
            if risposta_json["status"] == "ok":
                print(f"Risposta ricevuta correttamente. risposta: {risposta_json}")
        elif server == "echo":
            print("Inserire il testo:")
            text = await asyncio.to_thread(input)
            richiesta_diz = {
                "cmd": "echo",
                "text":text
            }
            richiesta_json = json.dumps(richiesta_diz) + "\n"
            writer.write(richiesta_json.encode())
            await writer.drain()

            risposta = await reader.readline()
            risposta_json = json.loads(risposta.decode())
            if risposta_json["status"] == "ok":
                print(f"Risposta ricevuta correttamente. risposta: {risposta_json}")
    except KeyboardInterrupt:
        print("Interruzione da tastiera")
    except Exception as e:
        print(f"Errore {e}")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print(f"Connessione con il server {server} terminata.")


async def main():
    try:
        await connessione_NameServer()
    except KeyboardInterrupt:
        print("Interruzione da tastiera")


if __name__ == "__main__":
    asyncio.run(main())
