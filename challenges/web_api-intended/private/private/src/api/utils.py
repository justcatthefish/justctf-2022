#! /usr/bin/env python3

# Utils


import random
import hashlib


def get_hexdigest(salt, raw_password):
    data = salt + raw_password
    return hashlib.sha1(data.encode('utf8')).hexdigest()


def make_password(raw_password):
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return f'{salt}${hsh}'


def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)