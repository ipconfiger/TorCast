what's it
===

this package can allows you to 	broadcast messages to another tornado process with redis pubsub function asynchronously,whatever they are in diffrent servers or not.

Quick start
===
1.Installation
---
use pip:
***
    pip install torcast
    
2.Use it
---
steps:
***

    from TorCast import client
    
    def on_message(chn, message):
        #call back function
        #do something when get message
        
    
    sub = client("127.0.0.1",6379,1) #create instance and setup redis connection
    sub.listen_to(['channel',],on_message) #regist channel and callback function
 
 
 full sample:
 ***
    import tornado.ioloop
    import tornado.web
    from TorCast import client
 
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")
 
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
 
    def on_message(chn, message):
        #when message recived, this function will be fired
 
    if __name__ == "__main__":
        application.listen(8888)
        sub = client("127.0.0.1",6379,1)
        sub.listen_to(["chn_1"],)
        tornado.ioloop.IOLoop.instance().start()
 
 More demo in demo folder 
 ---