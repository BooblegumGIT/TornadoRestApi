from schematics.types import StringType, EmailType
# from schematics.types.compound import ListType, DictType
# from schematics.exceptions import ModelValidationError
from base.models import BaseModel
from accounts.hashers import check_password, make_password


class UserModel(BaseModel):
    MONGO_COLLECTION = 'accounts'
    # DEFAULT_PERMISSIONS = {"news": ['read', ]}

    email = EmailType(required=True)
    password = StringType(required=True, min_length=3, max_length=50)
    password2 = StringType(required=True, min_length=3, max_length=50)
    first_name = StringType()
    last_name = StringType()
    # permissions = DictType(ListType, compound_field=StringType)

    # def __init__(self, *args, **kwargs):
    #     args[0]['_id'] = args[0].pop('email')
    #     BaseModel.__init__(self, *args, **kwargs)

    # @property
    # def email(self):
    #     print("get email")
    #     return self._id
    #
    # @email.setter
    # def email(self, value):
    #     print("set email")
    #     self._id = value

    @classmethod
    def process_query(cls, params):
        params = dict(params)
        if 'email' in params:
            params['_id'] = params.pop('email')
        return params

    def validate(self, *args, **kwargs):
        if self.password != self.password2:
            self.errors.add({"password2": ["пароли не совпадают"]})
        super(UserModel, self).validate(*args, **kwargs)

    def check_password(self, entered_password):
        return check_password(entered_password, self.password)

    def set_password(self, plaintext):
        self.password = make_password(plaintext)

    def get_data_for_save(self, ser):

        self._id = self.email
        self.set_password(self.password)
        data = ser or self.to_primitive()
        # if '_id' in data and data['_id'] is None:
        #     del data['_id']
        return data

    # def get_permissions(self, model):
    #     model_name = model.get_model_name()
    #     return self.permissions.get(model_name, [])

    # def has_permission(self, model, needed_permissions):
    #     user_permissions = set(self.get_permissions(model))
    #     return not (needed_permissions - user_permissions)

    # def insert(self, *args, **kwargs):
    #     if not self.permissions:
    #         self.permissions = dict(self.DEFAULT_PERMISSIONS)
    #     return super(UserModel, self).insert(*args, **kwargs)


if __name__ == "__main__":
    user = UserModel({'email': 'bla@mail.ru', 'password': 'pass'})
    # user.set_password('pass')
    user.save()
    if user.errors:
        print(user.errors)