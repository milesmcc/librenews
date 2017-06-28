import tornado.ioloop
import tornado.web
import httplib
import flashes
import configuration
import json
import arrow
import datetime
from userio import *

"""
You probably don't need to touch this file. Instead, hack away on the
templates and on `flashes.py`. But keep your hands away from this file
unless you're absolutely sure!
"""

class IndexHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)
    def get(self):
        say("Received INDEX request.")
        flash = flashes.get_latest_flashes(1)[0]
        time = str(flash['time'])
        if isinstance(flash['time'], basestring):
            time = arrow.Arrow.strptime(flash['time'], "%a %b %d %H:%M:%S +0000 %Y").humanize()
        elif isinstance(flash['time'], datetime.datetime):
            time = arrow.get(flash['time']).humanize()
        self.render("pages/index.html", flash=flash, time=time)
class ApiHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)
    def get(self):
        say("Received API request.")
        self.set_header("Content-Type", "application/json")
        data = {
            "server": "LibreNews Central",
            "channels": [k[1] for k in configuration.get_accounts()],
            "latest": flashes.get_latest_flashes(25)
        }
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class ErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)
    def get(self):
        self.render("pages/error.html", message="Page not found", error="404")
application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/api", ApiHandler),
    (r'/static/(.*)$', tornado.web.StaticFileHandler, {'path': "pages/static"})
    ], default_handler_class=ErrorHandler)
if __name__ == "__main__":
    flashes.go()
    ok("Starting webserver...")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
