import asyncio
import time

import websockets
from google.protobuf.json_format import MessageToDict

from node_launcher.logging import log
from tools.lnd_client import lnd_remote_client


async def hello(websocket, path):

    subscription = lnd_remote_client.subscribe_invoices(settle_index=1)

    for invoice in subscription:
        invoice_data = MessageToDict(invoice)
        log.debug('emit invoice', invoice=invoice)
        time.sleep(1)
        await websocket.send(invoice_data)


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
