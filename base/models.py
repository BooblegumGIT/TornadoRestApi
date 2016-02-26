import motor
import logging
from datetime import timedelta
from tornado import gen, ioloop
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure
from schematics.models import Model
from schematics.types import NumberType
from schematics.exceptions import ModelConversionError, ModelValidationError
from settings import MONGO_DB


l = logging.getLogger(__name__)


class BaseModel(Model):

    _id = NumberType(number_class=ObjectId, number_type="ObjectId")
    # errors = []

    def __init__(self, *args, **kwargs):
        self.errors = []
        self.set_db(kwargs.pop('db', None))
        if args[0].get("errors"):
            self.errors.append(args[0]['errors'])
        # игнорируем поля отсутствующие в модели
        try:
            super(BaseModel, self).__init__(*args, **kwargs)
        except ModelConversionError as error:
            args_dict = args[0]
            for key in error.messages.keys():
                del args_dict[key]
            print(args_dict)
            super(BaseModel, self).__init__(args_dict, *args, **kwargs)

    @property
    def db(self):
        return getattr(self, '_db', None)

    def set_db(self, db):
        self._db = db

    @classmethod
    def process_query(cls, query):
        """
        query can be modified here before actual providing to database.
        """
        return dict(query)

    @classmethod
    def get_collection(cls):
        return getattr(cls, 'MONGO_COLLECTION', None)

    @classmethod
    def check_collection(cls, collection):
        return collection or cls.get_collection()

    def get_data_for_save(self, ser):
        data = ser or self.to_primitive()
        if '_id' in data and data['_id'] is None:
            del data['_id']
        return data

    @gen.coroutine
    def save(self, db=None, collection=None, ser=None):
        """

        """
        try:
            self.validate()
        except ModelValidationError as error:
            self.errors.append(error.messages)
        # save Obj to DB
        db = db or self.db
        c = self.check_collection(collection)
        data = self.get_data_for_save(ser)
        # result = yield motor.Op(db[c].save, data)
        # return self, self.errors

        for i in self.reconnect_amount():
            try:
                result = yield motor.Op(db[c].save, data)
            except ConnectionFailure as e:
                exceed = yield self.check_reconnect_tries_and_wait(i, 'save')
                if exceed:
                    raise e
            else:
                self._id = result
                return self, self.errors

    @staticmethod
    def reconnect_amount():
        return range(MONGO_DB['reconnect_tries'] + 1)

    @classmethod
    @gen.coroutine
    def check_reconnect_tries_and_wait(cls, reconnect_number, func_name):
        if reconnect_number >= MONGO_DB['reconnect_tries']:
            raise gen.Return(True)
        else:
            timeout = MONGO_DB['reconnect_timeout']
            l.warning("ConnectionFailure #{0} in {1}.{2}. Waiting {3} seconds".format(
                reconnect_number + 1, cls.__name__, func_name, timeout))
            io_loop = ioloop.IOLoop.instance()
            yield gen.Task(io_loop.add_timeout, timedelta(seconds=timeout))

    @classmethod
    @gen.coroutine
    def find_one(cls, db, query, collection=None, model=True):
        result = None
        query = cls.process_query(query)
        for i in cls.reconnect_amount():
            try:
                result = yield motor.Op(
                    db[cls.check_collection(collection)].find_one, query)
            except ConnectionFailure as e:
                exceed = yield cls.check_reconnect_tries_and_wait(i, 'find_one')
                if exceed:
                    raise e
            else:
                if model and result:
                    result = cls.make_model(result, "find_one", db=db)
                raise gen.Return(result)