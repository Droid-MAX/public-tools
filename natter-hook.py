#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import json
import sys
import os

# Natter
protocol=sys.argv[1]
inner_ip=sys.argv[2]
inner_port=sys.argv[3]
outter_ip=sys.argv[4]
outter_port=sys.argv[5]

# Cloudflare
cf_api_token='CLOUDFLARE_API_TOKEN'
cf_zone_id='CLOUDFLARE_ZONE_ID'
cf_record_name='CLOUDFLARE_RECORD_NAME'
cf_service_name='_CLOUDFLARE_SERVICE_NAME'

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
            print(f"[Script] - Upload to server: {protocol}: {inner_ip}:{inner_port} -> {outter_ip}:{outter_port}")
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
    if not all([cf_api_token, cf_zone_id, cf_record_name, cf_service_name]):
        print("Missing one or more required variables.")
        exit(1)
    try:
        cf_record_id = get_record_id(cf_api_token, cf_zone_id, cf_record_name)
        update_response = update_cloudflare_dns(
            cf_api_token,
            cf_zone_id,
            cf_record_id,
            cf_record_name,
            f"{outter_ip}:{outter_port}",
            cf_service_name,
            f"_{protocol}",
        )
        print(json.dumps(update_response, indent=4))
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
