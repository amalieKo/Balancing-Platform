#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Locates ball on platform and sends the
X and Y coordinates over Modbus to assigned
slave on ip: 192.168.2.17, port: 502.

Code by: Magnus Øye, Dated: 06.11-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/Balancing-Platform
"""

# Importing packages
import cv2
from video_processing import ObjectDetection
from modbus_communication import ModbusClient
from joystick import Joystick

# Main loop
if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    cap.set(propId=3, value=640)
    cap.set(propId=4, value=480)

    client = ModbusClient()
    js = Joystick()
    objectDetection = ObjectDetection(cap, watch=True)

    # Sends data over Modbus client for as long the connection is established
    while client.isConnected():
        ball_coordinates = objectDetection.getCoordinates()
        js_coordinates = js.getEvents()
        client.sendInt(value=ball_coordinates[0], address=12288)
        client.sendInt(value=ball_coordinates[1], address=12290)
        client.sendInt(value=js_coordinates[0], address=12292)
        client.sendInt(value=js_coordinates[1], address=12294)

        # Break loop with ESC-key
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            objectDetection.stop()
            break
