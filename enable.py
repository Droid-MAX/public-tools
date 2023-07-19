#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import argparse
import serial
import serial.tools.list_ports

class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-d", "--interface", dest="ifaceName", metavar="<COM>", default=None,
            help="Specify the serial port device to use (*default=None)"
        )
        parser.add_argument(
            "-r", "--reboot", action="store_true", dest="needReboot", default=False,
            help="Reboot the device after the operation is complete (*default=False)"
        )
        group.add_argument(
            "-l", "--list-devs", action="store_true", dest="listDevices", default=False,
            help="List the serial port devices in the system (*default=False)"
        )
        return parser.parse_args()

opt = Parser().optparse()

iface = opt.ifaceName
reset = opt.needReboot
list_dev = opt.listDevices

ser = serial.Serial(
port = iface,
baudrate = 115200,
parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE,
bytesize = serial.EIGHTBITS,
timeout = 1
)

if list_dev:
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        sys.exit("[!] The serial port device not found!")
    else:
        for i in range(len(port_list)):
            plist = list(port_list[i])
            print(plist)
        ser.close()
        sys.exit()

def main():
    print("[+] Use serial port device:", ser.name)
    print("[+] Waiting for trigger code...")
    while(1):
        recv = ser.readline().decode()
        if recv.startswith('U-Boot'):
            print("[+] Received! sending interrupt command...")
            t_end = time.time() + 1
            while time.time() < t_end:
                ser.write(chr(0x03).encode())
            time.sleep(1)

            print("[+] Setting bootdelay as 3 second...")
            ser.write('setenv bootdelay 3\n'.encode())
            time.sleep(1)
            print("[+] Setting asc as 0...")
            ser.write('setenv asc 0\n'.encode())
            time.sleep(1)
            print("[+] Setting asc0 as 0...")
            ser.write('setenv asc0 0\n'.encode())
            time.sleep(1)
            print("[+] Setting preboot environment variable...")
            ser.write('setenv preboot "gpio input 105;gpio input 106;gpio input 107;gpio input 108;gpio set 3;gpio set 109;gpio set 110;gpio clear 423;gpio clear 422;gpio clear 325;gpio clear 402;gpio clear 424"\n'.encode())
            time.sleep(1)
            print("[+] Saving environment variables...")
            ser.write('saveenv\n'.encode())
            time.sleep(1)

            if reset:
                print("[+] Rebooting...")
                ser.write('reset\n'.encode())

            break

    ser.close()
    sys.exit()

if __name__ == '__main__': 
    try:
        main()
    except Exception as e:
        print("[!] Error:", e)
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        sys.exit(1)
