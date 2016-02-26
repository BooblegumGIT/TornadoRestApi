import logging
from schematics.types import StringType, EmailType
from schematics.types.compound import ListType, DictType
from schematics.exceptions import ModelValidationError
from base.models import BaseModel

l = logging.getLogger(__name__)
MAX_FIND_LIST_LEN = 100


class UserModel(BaseModel):
    MONGO_COLLECTION = 'users'
    email = EmailType(required=True)
    password = StringType(required=True, min_length=3, max_length=50)




    # @property
    # def email(self):
    #     return self._id
    #
    # @email.setter
    # def email(self, value):
    #     self._id = value
    #
    # @classmethod
    # def process_query(cls, params):
    #     params = dict(params)
    #     if 'email' in params:
    #         params['_id'] = params.pop('email')
    #     return params
    #
    # def validate(self, *args, **kwargs):
    #     try:
    #         return super(UserModel, self).validate(*args, **kwargs)
    #     except ModelValidationError as e:
    #         if '_id' in e.messages:
    #             e.messages['email'] = e.messages.pop('_id')
    #         raise


if __name__ == "__main__":
    user = UserModel(
        {
            'email': 'blabla.ru',
            'new': 'new'
        }
    )
    user.email = 'test@test.ru'

    print('user_model = ', user.get_collection())
    user, errors = user.save()
    if errors:
        print('errors = ', errors)
    print('user = ', user)
    # if not user.validate():
    #     print(user.errors)