#!/bin/sh
# Filename: edged.sh
# Date: 2021-7-21
# Version: 1.0
# Purpose: Use a simple way to control and manage edge service
# Author: Droid-MAX
# License: GPLv3

PATH=/usr/local/sbin:/usr/sbin:/sbin:$PATH

if [ $EUID != 0 ]; then
  sudo "$0" "$@"
  exit $?
fi

EDGE_NAME="edge"                           # Default Program Name (Require)
EDGE_IFACE="edge0"                         # Default Edge Interface Name (Require)
ETH_IFACE="eth0"                           # Default Ethernet Interface Name (Require)
NET_RANGE="10.0.1.0/24"                    # Default Edge Network Range (Consistent with HOST_ADDR, Require)
HOST_ADDR="10.0.1.1"                       # Default Edge Interface IPv4 Address (Consistent with NET_RANGE, Require)
NODE_NAME="TYPE_YOUR_NODE_NAME"            # Setting Your Edge Network Node Name (Require)
NODE_KEY="TYPE_YOUR_NODE_KEY"              # Setting Your Edge Network Node Key (Require)
SUPERNODE_ADDR="TYPE_YOUR_SUPERNODE_ADDR"  # Setting Your Supernode IPv4 Address (Require)

check_ipv4_forward(){
	if [ "$(cat /proc/sys/net/ipv4/ip_forward)" -eq "1" ]; then
		echo 1
	else
		echo 0
	fi
}

enable_ipv4_forward(){
	pre_checking_forward=$(check_ipv4_forward)
	if [ "$pre_checking_forward" -eq 0 ]; then
		echo 1 > /proc/sys/net/ipv4/ip_forward
	else
		echo "ipv4 forward already enabled on system..."
	fi
}

disable_ipv4_forward(){
	pre_checking_forward=$(check_ipv4_forward)
	if [ "$pre_checking_forward" -eq 1 ]; then
		echo 0 > /proc/sys/net/ipv4/ip_forward
	else
		echo "ipv4 forward already disabled on system..."
	fi
}

check_iptables_rule_exists(){
	if [ -z "$(iptables -vL | grep -i $EDGE_IFACE)" ]; then
		echo 1
	else
		echo 0
	fi
}

add_iptables_rules(){
	pre_existing_rule=$(check_iptables_rule_exists)
	if [ "$pre_existing_rule" -eq 1 ]; then
		iptables -A FORWARD -i $EDGE_IFACE -o $ETH_IFACE -j ACCEPT
		iptables -A FORWARD -i $ETH_IFACE -o $EDGE_IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
		iptables -t nat -A POSTROUTING -o $ETH_IFACE -s $NET_RANGE -j MASQUERADE
	else
		echo "iptables rules already exists on system..."
	fi
}

remove_iptables_rules(){
	pre_existing_rule=$(check_iptables_rule_exists)
	if [ "$pre_existing_rule" -eq 0 ]; then
		iptables -D FORWARD -i $EDGE_IFACE -o $ETH_IFACE -j ACCEPT
		iptables -D FORWARD -i $ETH_IFACE -o $EDGE_IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
		iptables -t nat -D POSTROUTING -o $ETH_IFACE -s $NET_RANGE -j MASQUERADE
	else
		echo "iptables rules already removed from system..."
	fi
}

do_start(){
	add_iptables_rules
	enable_ipv4_forward
	$EDGE_NAME -d $EDGE_IFACE -a $HOST_ADDR -c $NODE_NAME -k $NODE_KEY -l $SUPERNODE_ADDR -r > /dev/null 2>&1
}

do_stop(){
	killall $EDGE_NAME > /dev/null 2>&1
	remove_iptables_rules
#	disable_ipv4_forward
}

is_running(){
	if [ "`ps -ef | pgrep $EDGE_NAME | wc -l`" -eq "0" ]; then
		echo "$EDGE_NAME not running"
	else
		echo "$EDGE_NAME is running, pid is `ps -ef | pgrep $EDGE_NAME | xargs`"
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
