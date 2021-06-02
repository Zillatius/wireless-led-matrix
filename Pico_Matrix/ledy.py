import usys
import ustruct as struct
import utime
from machine import Pin, SPI
from NRF24L01 import NRF24L01, POWER_3, SPEED_1M, SPEED_250K
from micropython import const
import framebuf
import max7219matrix
from time import sleep
import urandom
from dht import DHT11, InvalidChecksum, InvalidPulseCount
import fb_slim_letters


def cellAuto(rule, buf):
    ruleArr = [(rule & (1 << x)) >> x for x in [0,1,2,3,4,5,6,7]]
    buf.scroll(0,-1)
    empty = 0
    for x in range(32):
        b = 0 | (buf.pixel((x-1)%32,30) << 2) | (buf.pixel(x,30) << 1) | (buf.pixel((x+1)%32,30))
        t = ruleArr[b]
        empty += t
        buf.pixel(x,31,t)
    if empty == 0:
        buf.pixel(urandom.randint(0,31),31,1)
    return buf


_RX_POLL_DELAY = const(10)
_SLAVE_SEND_DELAY = const(10)
pipes = (b"\xd2\xf0\xf0\xf0\xf0", b"\xe1\xf0\xf0\xf0\xf0")
ch_num = 120


ce = Pin(21, mode=Pin.OUT, value=0)
csn = Pin(9, mode=Pin.OUT, value=1)
spi = spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
nrf = NRF24L01(spi, csn, ce, payload_size=8, channel=ch_num)
nrf.set_power_speed(POWER_3, SPEED_250K)
nrf.reg_write(0x01, 0x3F)
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.start_listening()

cs_pin = 5
spi = SPI(0)
display = max7219matrix.Matrix8x8(spi=spi, cs=Pin(cs_pin), numx=4, numy=4)
display.brightness(0)
display.fill(0)
display.show()
buf = bytearray(8*4*4)

fb = framebuf.FrameBuffer(buf, 8 * 4, 8 * 4, framebuf.MONO_HLSB)

dhtpin = Pin(16, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(dhtpin)

temp = 0
hum = 0
cellType = 30
frameNum = 0
start_time = utime.ticks_ms()
try:
    while True:
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 100:
            start_time = utime.ticks_ms()
            try:
                temp = sensor.temperature
                hum = sensor.humidity
            except:
                pass
            fb = cellAuto(cellType,fb)
            display.blit(fb,0,0)
            display.rect(7,7,18,18,0)
            display.blit(fb_slim_letters.slim(temp // 10),8,8)
            display.blit(fb_slim_letters.slim(temp % 10 // 1),12,8)
            display.blit(fb_slim_letters.slim('deg'),16,8)
            display.blit(fb_slim_letters.slim('C'),20,8)
            display.blit(fb_slim_letters.slim(hum // 10),8,16)
            display.blit(fb_slim_letters.slim(hum % 10 // 1),12,16)
            display.fill_rect(16,16,8,8,0)
            display.text("%",16,16,1)
            display.show()

        if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                payload, = struct.unpack("<i", buf[:8])
                print("received:", payload)
                if cellType > 255 or cellType < 0:
                    cellType=payload
                utime.sleep_ms(_RX_POLL_DELAY)

            # Give master time to get into receive mode.
            nrf.stop_listening()
            utime.sleep_ms(2)
            tempRetry = 0
            while tempRetry < 5:
                try:
                    nrf.send(struct.pack("<ff", temp, hum))
                    tempRetry = 5
                    print("sent:{},{}".format(temp,hum))
                except:
                    tempRetry += 1
                    utime.sleep_ms(2)
            nrf.start_listening()
            
except KeyboardInterrupt:
    display.fill(0)
    display.show()