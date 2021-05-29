import sys
import time
import struct
from RF24 import RF24, RF24_PA_MIN, RF24_PA_MAX, RF24_250KBPS, RF24_1MBPS

def setCell(cellNum):
    temp = -1
    hum = -1
    radio.stopListening()
    buffer = struct.pack("<i", cellNum)
    result = radio.write(buffer)
    has_payload = False
    radio.startListening()
    timeout = False
    timestart = time.monotonic_ns()
    while not has_payload and not timeout:
        has_payload, pipe_num = radio.available_pipe()
        timeout = (time.monotonic_ns() - timestart) > 100000000
    if has_payload:
        buffer = radio.read(radio.payloadSize)
        temp,hum = struct.unpack("<ff", buffer)
    print("Received Temp: {} Hum: {}".format(temp,hum))
    return temp,hum

radio = RF24(22, 0)
if not radio.begin():
    raise RuntimeError("radio hardware is not responding")

address = [b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0"]

radio.setPALevel(RF24_PA_MAX)  # RF24_PA_MAX is default
radio.setChannel(120)
radio.setAutoAck(True)
radio.setDataRate(RF24_250KBPS)
radio.openWritingPipe(address[0])  # always uses pipe 0
radio.openReadingPipe(1, address[1])  # using pipe 1
radio.payloadSize = 8

