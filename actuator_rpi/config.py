# -*- coding: utf-8 -*-
import codecs
from configparser import SafeConfigParser
import os


class Config(object):
    def from_env(self, variable_name):
        rv = os.environ.get(variable_name)
        if not rv:
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)

        self.parser = SafeConfigParser()
        self.parser.readfp(codecs.open(rv, "r", "utf8"))

    def get(self, *args):
        return self.parser.get(*args)
