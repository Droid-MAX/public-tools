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
            "-i", "--ipaddr", dest="ipAddr", metavar="<IP>", default="192.168.1.10",
            help="Specify the devices ip address to use (*default='192.168.1.10')"
        )
        parser.add_argument(
            "-s", "--serverip", dest="serverIp", metavar="<IP>", default="192.168.1.2",
            help="Specify the server ip address to use (*default='192.168.1.2')"
        )
        parser.add_argument(
            "-f", "--image-name", dest="imageName", metavar="<IMG>", default="firmware",
            help="Specify the firmware image name to use, and the full filename should be '<imagename>-squashfs.image' (*default='firmware')"
        )
        group.add_argument(
            "-l", "--list-devs", action="store_true", dest="listDevices", default=False,
            help="List the serial port devices in the system (*default=False)"
        )
        return parser.parse_args()

opt = Parser().optparse()

iface = opt.ifaceName
dev_ip = opt.ipAddr
svr_ip = opt.serverIp
image_name = opt.imageName
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

            print("[+] Setting ipaddr as", dev_ip)
            ser.write('setenv ipaddr {a}\n'.format(a=dev_ip).encode())
            time.sleep(1)
            print("[+] Setting serverip as", svr_ip)
            ser.write('setenv serverip {b}\n'.format(b=svr_ip).encode())
            time.sleep(1)
            print("[+] Setting image name as", image_name)
            ser.write('setenv image_name {c}\n'.format(c=image_name).encode())
            time.sleep(1)
            print("[+] Saving environment variables...")
            ser.write('saveenv\n'.encode())
            time.sleep(1)
            print("[+] Sending firmware update command...")
            ser.write('run update_openwrt; reset\n'.encode())
            print("[+] Please be patient and wait for the device to reboot...")
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
