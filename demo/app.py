#coding=utf8
__author__ = 'Alexander.Li'
import sys
sys.path.append("..")
from TorCast import client
import tornado.ioloop
import tornado.web

class Chatroome(object):
    def __init__(self):
        self.user_requests = {}
        self.user_messages = {}

    def say_to_all(self, message):
        pass

hd = None

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        global hd
        hd = self


class MessageFetcher(tornado.web.RequestHandler):
    def get(self):
        print sub.notify_all("msg1", "test it!")
        self.write("done")
        self.finish()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/say", MessageFetcher),
])

def on_message(chn, data):
    hd.write(data)
    hd.finish()

if __name__ == "__main__":
    application.listen(int(sys.argv[1]))
    sub = client.Subscriber("127.0.0.1", 6379, 5)
    sub.listen_on(["msg1","msg2"], on_message)
    tornado.ioloop.IOLoop.instance().start()
