#!/usr/bin/env python3
import math
from cuesdk.helpers import ColorRgb
try:
    from cuesdk import CueSdk
except ModuleNotFoundError:
	raise RuntimeError("iCUE module not installed")
try:
	from spiceapi import *
except ModuleNotFoundError:
	raise RuntimeError("spiceapi module not installed")

def get_available_leds():
    leds = list()
    device_count = cue.get_device_count()

    for device_index in range(device_count):
        led_positions = cue.get_led_positions_by_device_index(device_index)
        leds.append(led_positions)

    return leds


def main():
    #Spice connection
    host = "192.168.9.201"
    port = 1234
    password = "5678"
    spice = Connection(host=host, port=port, password=password)

    #iCUE connection
    global cue
    cue = CueSdk()
    cue.connect()
    cue.request_control()

    devices = cue.get_devices()

    LightR = 0
    LightG = 0
    LightB = 0

    all_leds = get_available_leds()
    cnt = len(all_leds)

    break_program = False
    #get current RGB
    while break_program == False:
        LightsInfo = lights_read(spice)
        for light in LightsInfo:
            #get RGB info
            if light[0] == "Wing Left Up R":
                LightR = math.floor(light[1] * 255)
            elif light[0] == "Wing Left Up G":
                LightG = math.floor(light[1] * 255)
            elif light[0] == "Wing Left Up B":
                LightB = math.floor(light[1] * 255)
            else: continue

            #update the iCUE LED
            for di in range(cnt):
                buffer = dict()
                device_leds = all_leds[di]
                for led in device_leds:
                    buffer[led] = (LightR,LightG,LightB)
                cue.set_led_colors_buffer_by_device_index(di, buffer)
            cue.set_led_colors_flush_buffer()

if __name__ == "__main__":
    main()