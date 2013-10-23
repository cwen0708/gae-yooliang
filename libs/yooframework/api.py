#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encode_dict(my_dict):
    return "\x1e".join("%s\x1f%s" % x for x in my_dict.iteritems())

def decode_dict(my_string):
    return dict(x.split("\x1f") for x in my_string.split("\x1e"))


def validate_email(email):
    import re
    if len(email) > 6:
        if re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', email) is not None:
            return True
    return False

def random_string(length=8, use_ascii_letters=True, use_digits=True, use_punctuation=False):
    import string
    from random import choice
    characters = ""
    if use_ascii_letters:
        # 小寫
        characters += string.ascii_letters
    if use_digits:
        # 數字
        characters += string.digits
    if use_punctuation:
        # 符號
        characters += string.punctuation
    return "".join(choice(characters) for x in range(1, length))
