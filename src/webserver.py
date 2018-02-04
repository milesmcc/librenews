import datetime
import httplib
import json

import tornado
import tornado.ioloop
import tornado.web

import arrow
import configuration
import flashes
import stats
import push
from userio import error, ok, say


"""
You probably don't need to touch this file. Instead, hack away on the
templates and on `flashes.py`. But keep your hands away from this file
unless you're absolutely sure!
"""


def get_ip(request):
    x_real_ip = request.headers.get("X-Real-IP")
    remote_ip = x_real_ip or request.remote_ip
    return remote_ip


class IndexHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)

    def get(self):
        try:
            req_resp = stats.request(str(get_ip(self.request)))
        except:
            error("Errored while handling request IP -- still served...")
        say("Received INDEX request (" + req_resp + ")")
        alerts = flashes.get_latest_flashes(3)
        for flash in alerts:
            flash['text'] = tornado.escape.xhtml_unescape(flash['text'])
            if isinstance(flash['time'], basestring) and "+0000" in flash['time']:
                flash['time'] = arrow.Arrow.strptime(flash['time'], "%a %b %d %H:%M:%S +0000 %Y").humanize()
            if isinstance(flash['time'], datetime.datetime):
                flash['time'] = arrow.get(flash['time']).humanize()
        self.render("pages/index.html", flashes=alerts)

class StatsHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)

    def get(self):
        try:
            req_resp = stats.request(str(get_ip(self.request)))
            say("Received STATS request (" + req_resp + ")")
        except:
            error("Errored while handling request IP -- still served...")
        self.render("pages/stats.html", countries=stats.top_countries(), last_restart=stats.time(),
                    devices=stats.unique_devices(), total_requests=stats.requests,
                    requests_per_second=stats.requests_per_second())


class ApiHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)

    def get(self):
        try:
            req_resp = stats.request(str(get_ip(self.request)))
            say("Received API request (" + req_resp + ")")
        except:
            error("Errored while handling request IP -- still served...")
        self.set_header("Content-Type", "application/json")
        latest = -1
        try:
            latest = int(self.get_argument('latest'))
        except:
            pass  # no latest flash specified
        data = {
            "server": "LibreNews Central",
            "channels": [k[2] for k in configuration.get_accounts()],
            "latest": [flash for flash in flashes.get_latest_flashes(25)
                       if int(flash['id']) > int(latest)]
        }
        self.write(unicode(json.dumps(data, sort_keys=True, separators=(',', ':'))))


class ErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        try:
            stats.request(str(get_ip(self.request)))
        except:
            error("Errored while handling request IP -- still served...")
        self.render("pages/error.html", message=httplib.responses[status_code], error=status_code)

    def get(self):
        try:
            stats.request(str(get_ip(self.request)))
        except:
            error("Errored while handling request IP -- still served...")
        self.render("pages/error.html", message="Page not found", error="404")

class ServiceWorkerHandler(tornado.web.RequestHandler):
    def get(self):
        service_worker = """
self.addEventListener('push', function(event) {
    const notificationPromise = new Promise(function() {
        if (event.data) {
          fl = event.data.json()
          console.log('This push event has data: ', event.data.text());
          self.registration.showNotification(fl["channel"] + " - " + fl["source"], {
              body: fl["text"],
              timestamp: Date.parse(fl["time"]),
              data: fl
            });
        } else {
          console.log('This push event has no data.');
        }
    })

    const promiseChain = Promise.all([
        notificationPromise,
    ]);

    event.waitUntil(promiseChain);
});


self.addEventListener('notificationclick', function(event) {
    event.notification.close(); // Android needs explicit close.
    let url = event.notification.data["link"];
    event.waitUntil(
        clients.matchAll({type: 'window'}).then( windowClients => {
            // Check if there is already a window/tab open with the target URL
            for (var i = 0; i < windowClients.length; i++) {
                var client = windowClients[i];
                // If so, just focus it.
                if (client.url === url && 'focus' in client) {
                    return client.focus();
                }
            }
            // If not, then open the target URL in a new window/tab.
            if (clients.openWindow) {
                return clients.openWindow(url);
            }
        })
    );
});
        """
        self.write(service_worker)
        self.set_header("Content-Type", "application/javascript")
        self.finish()

class PushHandler(tornado.web.RequestHandler):
    def post(self):
        say("Receiving new subscription: " + self.request.body)
        self.set_header("Content-Type", "application/json")
        if push.register_new_receiver(tornado.escape.json_decode(self.request.body)):
            self.write(json.dumps({"response": "OK"}))
        else:
            self.write(json.dumps({"response": "REJECTED"}))
            self.status_code(400, reason="invalid subscription data")
        self.finish()

class BaseJavascriptHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/javascript")
        self.render("pages/base.js", applicationServerKey=push.get_application_server_key())

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/api", ApiHandler),
    (r"/stats", StatsHandler),
    (r"/push", PushHandler),
    (r"/base\.js", BaseJavascriptHandler),
    (r'/service-worker\.js', ServiceWorkerHandler),
    (r'/static/(.*)$', tornado.web.StaticFileHandler, {'path': "pages/static"}),
    ], default_handler_class=ErrorHandler)
if __name__ == "__main__":
    flashes.go()
    ok("Starting webserver...")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
