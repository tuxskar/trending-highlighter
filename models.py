import datetime
from collections import OrderedDict

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
    def to_json(self):
        to_ret = {}
        for key in self.keys():
            to_ret[key] = [x.to_json() for x in self.get(key)]
        return to_ret


MessagesCollection = MessagesCollection()

_users = OrderedDict()


def get_users():
    if not _users:
        user_names = ['peter', 'jon', 'joakim', 'juan', 'fran', 'pepe', 'penelope', 'maria', 'ana', 'monica']
        colors = ["#B4D75F", "#364F86", "#0AA594", "#0063AF", "#45C5E5", "#BE4856", "#DD9D9D", "#EBECEC", "#D1D3D4",
                  "#31ADED", "#ED4035", "#ED9743"]
        for username, color in zip(user_names, colors):
            _users[username] = color
    return _users
