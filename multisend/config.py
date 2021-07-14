import json
import py

class Config(dict):

    PATH = None

    def __init__(self, *args, **kwargs):
        self.config = py.path.local(self.PATH).join('config.json')
        print(self.config)
        super(Config, self).__init__(*args, **kwargs)
        self.load()

    def load(self):
        """load a JSON config file from disk"""
        try:
            self.update(json.loads(self.config.read()))
        except py.error.ENOENT:
            pass