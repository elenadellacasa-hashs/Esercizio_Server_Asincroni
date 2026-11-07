import json
import asyncio
import sys

async def connessione_NameServer():
    try:
        while True:
            if len(sys.argv) < 2:
                print("Errore!!! non abbastanza argomenti inseriti. Formattazione corretta: python nome_file.py nome_server")
                return
            server = sys.argv[1]
            reader, writer = await asyncio.open_connection('127.0.0.1',6000)  # per aprire una connessione in modo asincrono
            richiesta_diz = {
                "cmd" : "lookup",
                "service" : server
            }
            richiesta_json = json.dumps(richiesta_diz) + "\n"

            writer.write(richiesta_json.encode())
            await writer.drain()

            risposta = await reader.readline()
            risposta_json = json.loads(risposta.decode())

            if risposta_json["status"] == "ok":
                writer.close()
                await writer.wait_closed()
    except KeyboardInterrupt:
        print("Interruzione da tastiera")
    except Exception as e:
        print(f"Errore!! {e}")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print("Connessione terminata")


