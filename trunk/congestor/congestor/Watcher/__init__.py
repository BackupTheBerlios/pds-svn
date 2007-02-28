# -*- encoding:utf8

from os import name
import sys

def _creator(name):
    return lambda options : \
        __import__(__name__ + "." + options[name.lower()]["type"],{}, {}, name) \
        .__dict__[name](options[name.lower()])

Watcher = _creator("Watcher")
