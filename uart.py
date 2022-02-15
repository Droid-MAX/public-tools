#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import serial
import serial.tools.list_ports

port_list = list(serial.tools.list_ports.comports())
if len(port_list) <= 0:
    print("[-] The serial port device not found!")
    sys.exit(1)
else:
    try:
        plist = list(port_list[0])
        serialName = plist[0]
        ser = serial.Serial(
        port = serialName,
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )
        print("[+] Use serial port device:", ser.name)

        print("[+] Wait for trigger signal...")
        while(1):
            if (ser.inWaiting() != 0):
                print("[+] Start send command...")
                ser.write(chr(0x03).encode())
                time.sleep(1)
                ser.write('setenv ipaddr 192.168.1.10\n'.encode())
                time.sleep(1)
                ser.write('setenv serverip 192.168.1.2\n'.encode())
                time.sleep(1)
                ser.write('setenv image_name firmware.bin\n'.encode())
                time.sleep(1)
                ser.write('save\n'.encode())
                time.sleep(3)
                ser.write('run update_openwrt\n'.encode())
                print("[+] Command send complete!")
                break

        ser.close()
        sys.exit(0)

    except Exception as e:
        print("[!] Error:", e)
