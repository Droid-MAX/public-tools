#!/bin/sh
# Filename: supernoded.sh
# Date: 2021-7-21
# Version: 1.0
# Purpose: Use a simple way to control and manage supernode service
# Author: Droid-MAX
# License: GPLv3

PATH=/usr/local/sbin:/usr/sbin:/sbin:$PATH

SUPERNODE_NAME="supernode"      # Default Program Name (Require)
UDP_PORT="7777"                 # Default Listening Port (Require)
LOG_PREFIX="/var/log"           # Default Log Save Folder (Require)
LOG_NAME="$SUPERNODE_NAME.log"  # Default Log Filename (Require)
LOG_PATH=$LOG_PREFIX/$LOG_NAME  # Default Log Save Path (Require)

check_iptables_rule_exists(){
	if [ -z "$(iptables -vL | grep -i $UDP_PORT)" ]; then
		echo 1
	else
		echo 0
	fi
}

add_iptables_rules(){
	pre_existing_rule=$(check_iptables_rule_exists)
	if [ "$pre_existing_rule" -eq 1 ]; then
		iptables -A INPUT -p udp --dport $UDP_PORT -j ACCEPT
	else
		echo "iptables rules already exists on system..."
	fi
}

remove_iptables_rules(){
	pre_existing_rule=$(check_iptables_rule_exists)
	if [ "$pre_existing_rule" -eq 0 ]; then
		iptables -D INPUT -p udp --dport $UDP_PORT -j ACCEPT
	else
		echo "iptables rules already removed from system..."
	fi
}

do_start(){
	add_iptables_rules
	$SUPERNODE_NAME -l $UDP_PORT >> $LOG_PATH 2>&1 &
}

do_stop(){
	killall $SUPERNODE_NAME > /dev/null 2>&1
	remove_iptables_rules
}

is_running(){
	if [ "`ps -ef | pgrep $SUPERNODE_NAME | wc -l`" -eq "0" ]; then
		echo "$SUPERNODE_NAME not running"
	else
		echo "$SUPERNODE_NAME is running, pid is `ps -ef | pgrep $SUPERNODE_NAME | xargs`"
	fi
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
	    sleep 2
	    do_start
	    ;;
	status)
	    is_running
	    ;;
	*)
            echo "Usage: $0 {start|stop|restart|status}"
            exit 1
            ;;
esac
