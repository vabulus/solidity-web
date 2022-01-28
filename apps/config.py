import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Debug': DebugConfig
}
