import sys
import logging
import asyncio
import threading
import random
from typing import Any, Union

from bless import (
    BlessServer, BlessGATTCharacteristic,GATTCharacteristicProperties, GATTAttributePermissions)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use threading for macOS and Windows, asyncio for Linux
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    trigger = threading.Event()
else:
    trigger = asyncio.Event()


def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
    logger.debug(f"Reading characteristic: {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    logger.debug(f"Write received: {value}")
    characteristic.value = value
    if value == b"\x01":  # Signal to start streaming
        logger.info("Start signal received. Beginning EMG stream...")
        trigger.set()


async def stream_emg_data(server, service_uuid: str, char_uuid: str):
    for batch_num in range(6):  # x batches over 5 seconds
        raw_values = [random.randint(0, 3300) for _ in range(500)]
        
        # Send as chunks of 10 bytes (20 bytes total)
        for i in range(0, len(raw_values), 10):
            chunk = raw_values[i:i + 10]
            data = bytearray()
            for sample in chunk:
                data += sample.to_bytes(2, 'little') # 2 bytes in little endian
                    
            server.get_characteristic(char_uuid).value = data
            server.update_value(service_uuid,char_uuid)
            await asyncio.sleep(0.05)  # ~50 chunks/sec (1000 samples/sec)

        logger.info(f"Sent batch {batch_num + 1}")
        await asyncio.sleep(0.5)  # Wait before next batch


async def run(loop):
    trigger.clear()
    my_service_name = "MuscleMax Pi Service"
    
    server = BlessServer(name=my_service_name, loop=loop)
    server.read_request_func = read_request
    server.write_request_func = write_request

    service_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
    await server.add_new_service(service_uuid)
    
    char_uuid = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"

    char_flags = (
        GATTCharacteristicProperties.read
        | GATTCharacteristicProperties.write
        | GATTCharacteristicProperties.notify        
    )
    perms = GATTAttributePermissions.readable | GATTAttributePermissions.writeable

    await server.add_new_characteristic(service_uuid, char_uuid, char_flags, None, perms)

    logger.debug(server.get_characteristic(char_uuid))
    await server.start()
    logger.info("BLE advertising. Waiting for start signal (write 0x01)...")

    if trigger.__module__ == "threading":
        trigger.wait()
    else:
        await trigger.wait()
    
    await asyncio.sleep(2)
    logger.debug("Updating")
    server.get_characteristic(char_uuid)
    server.update_value(service_uuid, "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B")
    await stream_emg_data(server, service_uuid, char_uuid)
    await asyncio.sleep(5)
    await server.stop()
    logger.info("Server stopped.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
