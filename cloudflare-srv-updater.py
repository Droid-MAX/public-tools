#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import requests
import json
import sys
import os

class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-a", "--cf_api_token", dest="apiToken", metavar="cf_api_token", required=True,
            help="specify the cloudflare api token (required)"
        )
        parser.add_argument(
            "-i", "--cf_zone_id", dest="zoneId", metavar="cf_zone_id", required=True,
            help="specify the cloudflare zone id (required)"
        )
        parser.add_argument(
            "-s", "--cf_srv_name", dest="srvName", metavar="cf_srv_name", required=True,
            help="specify the cloudflare service name, example: '_CLOUDFLARE_SERVICE_NAME' (required)"
        )
        parser.add_argument(
            "-n", "--cf_domain_name", dest="domainName", metavar="cf_domain_name", required=True,
            help="specify the cloudflare domain name (required)"
        )
        parser.add_argument(
            "-m", "--protocol", dest="proto", metavar="protocol", default="tcp",
            help="specify the protocol, 'tcp' or 'udp' (default: tcp)"
        )
        parser.add_argument(
            "-t", "--host", dest="host", metavar="host", required=True,
            help="specify the host name (required)"
        )
        parser.add_argument(
            "-p", "--port", dest="port", metavar="port", required=True,
            help="specify the port number (required)"
        )
        return parser.parse_args()

opt = Parser().optparse()

cf_api_token = opt.apiToken
cf_zone_id = opt.zoneId
cf_srv_name = opt.srvName
cf_domain_name = opt.domainName
protocol = opt.proto
host = opt.host
port = opt.port

cf_record_name = f'{cf_srv_name}._{protocol}.{cf_domain_name}'

def get_record_id(api_token, zone_id, record_name):
    url = (
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    )
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(url, headers=headers)
        if not json.loads(response.text)['success']:
            return None
        domains = json.loads(response.text)['result']
        for domain in domains:
            if record_name == domain['name']:
                return domain['id']
        print("Record name is invalid.")
        exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def update_cloudflare_dns(
        api_token, zone_id, record_id, name, content, service, proto, ttl=60
):
    url = (
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    )
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "SRV",
        "name": name,
        "content": content,
        "data": {
            "service": service,
            "proto": proto,
            "name": name,
            "priority": 0,
            "weight": 0,
            "port": int(content.split(":")[1]),
            "target": content.split(":")[0],
        },
        "ttl": ttl,
    }
    try:
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Updated SRV record to Cloudflare: {cf_record_name} -> {host}:{port}")
        else:
            print(f"Error updating Cloudflare DNS: HTTP {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    # if not all([cf_api_token, cf_zone_id, cf_srv_name, cf_record_name, host]):
        # print("Missing one or more required variables.")
        # exit(1)
    try:
        cf_record_id = get_record_id(cf_api_token, cf_zone_id, cf_record_name)
        update_response = update_cloudflare_dns(
            cf_api_token,
            cf_zone_id,
            cf_record_id,
            cf_domain_name,
            f"{host}:{port}",
            cf_srv_name,
            f"_{protocol}",
        )
        # print(json.dumps(update_response, indent=4))
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
