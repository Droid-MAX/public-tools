#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import serial
import serial.tools.list_ports

port_list = list(serial.tools.list_ports.comports())
if len(port_list) <= 0:
    sys.exit("[!] The serial port device not found!")
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

        print("[+] Waiting for trigger characters...")
        while(1):
            recv = ser.readline().decode()
            if recv.startswith('U-Boot'):
                print("[+] Received! transfer upgrade command...")
                print("[+] Transfer command sequence 1")
                t_end = time.time() + 3
                while time.time() < t_end:
                    ser.write(chr(0x03).encode())
                time.sleep(1)
                print("[+] Transfer command sequence 2")
                ser.write('setenv ipaddr 192.168.1.10\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 3")
                ser.write('setenv serverip 192.168.1.2\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 4")
                ser.write('setenv image_name firmware\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 5")
                ser.write('save\n'.encode())
                time.sleep(3)
                print("[+] Transfer command sequence 6")
                ser.write('run update_openwrt; reset\n'.encode())
                print("[+] Upgrade command transfer complete! please wait for reboot...")
                break

        ser.close()
        sys.exit()

    except Exception as e:
        print("[!] Error:", e)
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        sys.exit(1)
