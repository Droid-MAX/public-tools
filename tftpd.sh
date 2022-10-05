#!/system/bin/sh
export PATH=/sbin:/system/sbin:/system/bin:/system/xbin

DAEMON_NAME="udpsvd"
ADDR="0.0.0.0"
PORT="69"
SRV_NAME="tftpd"
EXEC_OPT="-vE $ADDR $PORT $SRV_NAME $WORK_DIR"

check_args(){
	if [ -z $2 ]; then
		WORK_DIR="."
	else
		WORK_DIR=$2
	fi
	return 0
}

do_start(){
	check_args
	nohup $DAEMON_NAME $EXEC_OPT > /dev/null 2>&1 &
	echo "$SRV_NAME service started"
	exit 0
}

do_stop(){
	pkill -9 $DAEMON_NAME > /dev/null 2>&1
	echo "$SRV_NAME service stopped"
	exit 0
}

is_running(){
	PID=$(pgrep $DAEMON_NAME)
	if [ -z $PID ]; then
		echo "$SRV_NAME service not running"
	else
		echo "$SRV_NAME service is running, pid is $PID"
	fi
	exit 0
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
		echo "Usage: $0 {start|stop|status} <path, default: current folder>"
		exit 1
		;;
esac
