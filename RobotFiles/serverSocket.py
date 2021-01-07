import tornado.ioloop
import tornado.web
import asyncio
import json


class MainHandler(tornado.web.RequestHandler):
  def initialize(self, data):
      self.data = data
      
  def get(self):
      if self.data["receivedData"] == "false":
          self.write(json.dumps(self.data["coordinates"]))
      else:
          self.write(json.dumps(self.data))
          
      
      
  def post(self):
      data = self.get_argument("data")
      self.data["receivedData"] = "true"
      self.data["initData"] = data

      
      
def make_app(appData):
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = tornado.web.Application([
        (r"/", MainHandler, dict(data=appData)),
        ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    make_app({})
    