# -*- coding: utf-8 -*-
"""Password processing mostly taken from
https://github.com/hmarr/mongoengine/blob/master/mongoengine/django/auth.py
"""
# from django.utils.encoding import smart_str
# from django.utils.hashcompat import md5_constructor, sha_constructor
import hashlib
import uuid


def get_hexdigest(algorithm, salt, raw_password):
    # raw_password, salt = smart_str(raw_password), smart_str(salt)
    # if algorithm == 'md5':
    #     return md5_constructor(salt + raw_password).hexdigest()
    if algorithm == 'sha512':
        # return sha_constructor(salt + raw_password).hexdigest()
        # print('raw_password = ', raw_password)
        # print('salt = ', salt)
        return hashlib.sha512((salt + raw_password).encode('utf-8')).hexdigest()
    raise ValueError('Got unknown password algorithm type in password')


def check_password(raw_password, password):
    algo, salt, hash = password.split('$')
    return hash == get_hexdigest(algo, salt, raw_password)


def make_password(raw_password):
    algo = 'sha512'
    salt = uuid.uuid4().hex
    hash = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hash)
