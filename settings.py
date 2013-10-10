# -*- coding: utf-8 -*-

import json
import os
import core
import codecs

path = core.storage("settings.json")

def load():
    if not os.path.exists(path):
        blank = {}
        with codecs.open(path, "w", "utf-8") as f:
            json.dump(blank, f)
            return blank
    with codecs.open(path, "r", "utf-8") as f:
        return json.load(f)

def set(**kwargs):
    settings = load()
    for (k, v) in kwargs.iteritems():
        settings[k] = v
    with codecs.open(path, "w", "utf-8") as f:
        json.dump(settings, f)

def get(k, default=None):
    try:
        return load()[k]
    except KeyError:
        return default
