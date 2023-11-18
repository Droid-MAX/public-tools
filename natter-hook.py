#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import json
import sys
import os

# Cloudflare
cf_api_token='adfh8adf7ygaeruhngiadufhb9dfp98gudfg'
cf_zone_id='gouiadfyg87argahrd87rghdo8fg7hdfo8g7h'
cf_record_id='lkw45jh6klrjyhlrisufgh9adfgh7aidybfg'
cf_record_name='cleverly-named-subdomain'
cf_service_name='_cleverly-named-service'

# Natter
protocol=sys.argv[1]
inner_ip=sys.argv[2]
inner_port=sys.argv[3]
outter_ip=sys.argv[4]
outter_port=sys.argv[5]

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
        if response.status_code != 200:
            print(f"Error updating Cloudflare DNS: HTTP {response.status_code}")
            print(response.json())
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    if not all([cf_api_token, cf_zone_id, cf_record_id]):
        print("Missing one or more required variables.")
        exit(1)

    if inner_ip and inner_port and outter_ip and outter_port:
        print(f"[Script] - Upload to server: {protocol}: {inner_ip}:{inner_port} -> {outter_ip}:{outter_port}")
        update_response = update_cloudflare_dns(
            cf_api_token,
            cf_zone_id,
            cf_record_id,
            cf_record_name,
            f"{outter_ip}:{outter_port}",
            cf_service_name,
            "_{protocol}",
        )
        print(json.dumps(update_response, indent=4))
    else:
        print("Failed to retrieve host and port.")
