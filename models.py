import datetime
from collections import OrderedDict, defaultdict

import attr


def default_now():
    return datetime.datetime.now().isoformat()


@attr.s
class Message(object):
    username = attr.ib()
    msg = attr.ib()
    timestamp = attr.ib(default=attr.Factory(default_now))

    def to_json(self):
        return attr.asdict(self)


class MessagesCollection(dict):
    def to_json(self, key=None):
        to_ret = {}
        if key:
            if self.get(key):
                return [x.to_json() for x in self.get(key)]
            return []
        for key in self.keys():
            to_ret[key] = [x.to_json() for x in self.get(key)]
        return to_ret


MessagesCollection = MessagesCollection()

_users = OrderedDict()


def get_users():
    if not _users:
        user_names = ['peter', 'jon', 'joakim', 'juan', 'fran', 'pepe', 'penelope', 'maria', 'ana', 'monica']
        # colors = ["#B4D75F", "#364F86", "#0AA594", "#0063AF", "#45C5E5", "#BE4856", "#DD9D9D", "#EBECEC", "#D1D3D4",
        #           "#31ADED", "#ED4035", "#ED9743"]
        colors = ["rgb(247, 202, 201)", "rgb(247, 120, 107)", "rgb(145, 168, 208)", "rgb(3, 79, 132)",
                  "rgb(250, 224, 60)", "rgb(152, 221, 222)", "rgb(152, 150, 164)", "rgb(221, 65, 50)",
                  "rgb(177, 143, 106)", "rgb(121, 199, 83)"]
        for username, color in zip(user_names, colors):
            _users[username] = color
    return _users


WordCounter = defaultdict(int)
