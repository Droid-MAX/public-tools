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
                print("[+] Received! transfer enable command...")
                print("[+] Transfer command sequence 1")
                t_end = time.time() + 3
                while time.time() < t_end:
                    ser.write(chr(0x03).encode())
                time.sleep(1)
                print("[+] Transfer command sequence 2")
                ser.write('setenv bootdelay 3\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 3")
                ser.write('setenv asc 0\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 4")
                ser.write('setenv asc0 0\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 5")
                ser.write('setenv preboot "gpio input 105;gpio input 106;gpio input 107;gpio input 108;gpio set 3;gpio set 109;gpio set 110;gpio clear 423;gpio clear 422;gpio clear 325;gpio clear 402;gpio clear 424"\n'.encode())
                time.sleep(1)
                print("[+] Transfer command sequence 6")
                ser.write('saveenv\n'.encode())
                time.sleep(3)
                print("[+] Transfer command sequence 7")
                ser.write('reset\n'.encode())
                print("[+] Enable command transfer complete! rebooting...")
                break

        ser.close()
        sys.exit()

    except Exception as e:
        print("[!] Error:", e)
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        sys.exit(1)
