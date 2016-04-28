from base.handlers import BaseHandler
from tornado import gen


class TestHandler(BaseHandler):
    def get(self, *args, **kwargs):
        print("get", args, kwargs)
        self.render_json({"errors": False})

    @gen.coroutine
    def post(self, *args, **kwargs):
        print("post", args, kwargs)