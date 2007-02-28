# -*- coding:utf-8 -*-
#\todo Die Möglichkeit von Standardoptionen
def _creator(name):
    return lambda options : \
            __import__(__name__ + "." + options[name.lower()]["type"],{},{}, name) \
            .__dict__[name](options[name.lower()])

Storage = _creator("Storage")
Cache = _creator("Cache")
