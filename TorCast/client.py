#coding=utf8
__author__ = 'Alexander.Li'
import logging
import socket
import tornado.ioloop
import tornado.iostream
from tornado.iostream import StreamClosedError

def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)

class Connection(object):
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(sock)
        stream.connect((host, port))
        self.stream = stream
        self.channels = []
        self.when_line = None

    def subscribe(self, *channels):
        for chn in channels:
            if chn not in self.channels:
                self.channels.append(chn)

    def regist_trigger(self, on_line):
        self.when_line = on_line


    def write(self, command):
        self.stream.write(str(command))

    def recive(self):
        def on_line(data):
            self.when_line(data[:-2])
            self.recive()
        self.stream.read_until("\r\n", on_line)


class CommandParser(object):
    def __init__(self, command, *argvs):
        self.params = [command,] + list(argvs)

    def __repr__(self):
        output = ["*%s"%len(self.params)]
        for p in self.params:
            output.append("$%s"%len(p))
            output.append(p)
        output.append("\r\n")
        command_str = "\r\n".join(output)
        return command_str

class Subscriber(object):
    def __init__(self, host, port, db):
        self.conn_params = (host,port,db)
        self.reconnect(*self.conn_params)
        self.data_pool = []
        self.param_len = -1
        self.callback = None
        self.channels = None
        self.state_ok = False

    def listen_on(self, channels, callback):
        self.conn.write(CommandParser("subscribe", *channels))
        self.callback = callback
        self.channels = channels

    def reconnect(self, host, port, db):
        def on_line(data):
            self.on_data(data)
        def silent(data):
            pass
        self.conn = Connection(host, port)
        self.conn.regist_trigger(on_line)
        self.conn.write(CommandParser("SELECT",str(db)))
        self.conn.recive()
        self.send_conn = Connection(host, port)
        self.send_conn.regist_trigger(silent)
        self.send_conn.write(CommandParser("SELECT",str(db)))
        self.send_conn.recive()
        self.state_ok = True


    def on_data(self, data):
        if data[0] == "*":
            del self.data_pool[:]
            self.param_len = int(data[1:])*2
        else:
            if len(self.data_pool)<=self.param_len:
                self.data_pool.append(data)
            if len(self.data_pool)==self.param_len:
                message = [data for data in self.data_pool if data[0]!="$"]
                del self.data_pool[:]
                if message[0] == "message":
                    self.callback(message[1],message[2])

    def check_connection(self):
        if not self.state_ok:
            self.reconnect(*self.conn_params)
            self.conn.write(CommandParser("subscribe", *self.channels))


    def notify_all(self, channel, message):
        if channel not in self.channels:
            return False
        try:
            self.send_conn.write(CommandParser("publish", channel, tob(message)))
        except StreamClosedError, e:
            logging.error(e.message)
            self.state_ok = False
            return False
        return True
