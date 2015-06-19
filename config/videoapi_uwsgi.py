[uwsgi]
#application's base folder, 部署时，应该把它修改到测评代码根目录位置
wsgi-file = /opt/webroot/videodownload/videoapi.py

#the variable that holds a flask application
callable = app

process = 4
threads = 2

#home = %(base)
#pythonpath = /usr/local/bin/python3

#socket file's location
socket = /var/run/%n.sock
#web standalone mode
#http = 0.0.0.0:3031

#permissions for the socket file
chmod-socket = 666

#location of log files
#logto = /var/log/uwsgi/%n.log
