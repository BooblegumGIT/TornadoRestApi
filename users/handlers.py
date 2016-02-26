import logging
import json
from tornado import gen
from users.models import UserModel
from base.handlers import BaseHandler
from bson.objectid import ObjectId
from schematics.exceptions import ModelConversionError, ModelValidationError

l = logging.getLogger(__name__)

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


class RegisterHandler(BaseHandler):
    def initialize(self, **kwargs):
        super(RegisterHandler, self).initialize(**kwargs)
        self.db = self.settings['db']

    def get(self):
        self.write('GET: OK')

    @gen.coroutine
    def post(self):
        user = UserModel(self.json)
        user.set_db(self.db)
        # print(user.errors)
        user, errors = yield user.save()
        if errors:
            self.render_json(errors)
            print('errors = ', errors)

        print('user = ', user.to_primitive())
        self.render_json(user.to_primitive())

        # self.render_json({"result": "OK"})