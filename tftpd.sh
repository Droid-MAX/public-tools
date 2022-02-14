#!/bin/sh

PATH=/usr/local/sbin:/usr/sbin:/sbin:$PATH

if [ $EUID != 0 ]; then
  sudo "$0" "$@"
  exit $?
fi

EXEC_NAME="udpsvd"
ADDR="0.0.0.0"
PORT="69"
NAME="tftpd"
DIR=$2
EXEC_OPT="-vE $ADDR $PORT $NAME $DIR"

check_args(){
	if [ -z $DIR ]; then
		DIR="."
	fi
	return 0
}

do_start(){
	check_args
	nohup $EXEC_NAME $EXEC_OPT &
	echo "tftpd service started"
	exit 0
}

do_stop(){
	killall $EXEC_NAME > /dev/null 2>&1
	echo "tftpd service stopped"
	exit 0
}

is_running(){
	if [ "`ps -ef | pgrep $EXEC_NAME | wc -l`" -eq "0" ]; then
		echo "tftpd service not running"
	else
		echo "tftpd service is running, pid is `ps -ef | pgrep $EXEC_NAME | xargs`"
	fi
}

case "$1" in
	start)
		do_start
		;;
	stop)
		do_stop
		;;
	status)
		is_running
		;;
	*)
		echo "Usage: $0 {start|stop|status} <path>"
		exit 1
		;;
esac
