APPNAME=launcher

# user name 
USER=launcher
# path to home dir
PATH_HOME=/home/launcher

PATH=/bin:/usr/bin:/sbin:/usr/sbin
ACTIVATE=$PATH_HOME/.virtualenvs/launcher/bin/activate
APPMODULE=backend.wsgi:application
DAEMON=$PATH_HOME/.virtualenvs/launcher/bin/gunicorn
BIND=127.0.0.1:4020
PIDFILE=/var/run/gunicorn_launcher.pid
LOGFILE=$PATH_HOME/run_launcher.log
WORKERS=4
PATH_APP=$PATH_HOME/www/backend

. /lib/lsb/init-functions


if [ -e "/etc/default/$APPNAME" ]
then
    . /etc/default/$APPNAME
fi


case "$1" in
  start)
        log_daemon_msg "Starting deferred execution scheduler" "$APPNAME"
        source $ACTIVATE
        $DAEMON --daemon --chdir $PATH_APP --bind=$BIND --pid=$PIDFILE --workers=$WORKERS --user=$USER --log-file=$LOGFILE $APPMODULE
        log_end_msg $?
    ;;
  stop)
        log_daemon_msg "Stopping deferred execution scheduler" "APPNAME"
        killproc -p $PIDFILE $DAEMON
        log_end_msg $?
    ;;
  force-reload|restart)
    $0 stop
    $0 start
    ;;
  status)
    status_of_proc -p $PIDFILE $DAEMON && exit 0 || exit $?
    ;;
  *)
    echo "Usage: /etc/init.d/$APPNAME {start|stop|restart|force-reload|status}"
    exit 1
    ;;
esac

exit 0
