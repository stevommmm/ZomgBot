import os, sys, yaml, copy

DEFAULT = {
    "irc": {
        "nick":     "ZomgBot",
        "channels": ["#llama"],
        "server":   "irc.gamesurge.net",
        "port":     6667,
        "ssl":      False,
    },
    "bot": {
        "admins":   ["edk141", "Deaygo"],
        "plugins":  ["ban_manager", "util"],
    },
}

class Config(dict):
    def __init__(self, fn="config.yml", init={}):
        self.update(init)
        self.filename = fn

    def save(self):
        with open(self.filename, 'w') as f:
            yaml.dump(dict(**self), f, default_flow_style=False)

    def threaded_save(self):
        from twisted.internet import reactor
        def _save(d):
            try:
                with open(self.filename, 'w') as f:
                    yaml.dump(d, f, default_flow_style=False)
            except: raise
        reactor.callInThread(_save, copy.deepcopy(dict(**self)))

    def _load(self):
        with open(self.filename, 'r') as f:
            self.update(yaml.load(f))
    
    def _create(self):
        with open(self.filename, 'w') as f:
            yaml.dump(DEFAULT, f)

    def loadOrCreate(self):
        if os.path.exists(self.filename):
            self._load()
        else:
            self._create()
            sys.exit(1)
