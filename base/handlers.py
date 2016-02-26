import tornado.web
from tornado import gen
# import json
import bson.json_util


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        super(BaseHandler, self).initialize(**kwargs)
        self.db = self.settings['db']
        self.current_user = None

    def render_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(bson.json_util.dumps(data))

    @property
    def json(self):
        try:
            return bson.json_util.loads(self.request.body.decode('utf-8'))
        except ValueError:
            return {"errors": "data mast be in JSON Format"}

    @gen.coroutine
    def get_current_user(self):
        from users.models import UserModel
        email = self.current_user
        if email:
            # TODO cache
            user = yield UserModel.find_one(self.db, {"email": email})
        else:
            user = None
        self.current_user = user
        raise gen.Return(user)