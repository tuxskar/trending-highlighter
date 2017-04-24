import datetime

import attr


def default_now():
    return datetime.datetime.utcnow().isoformat()


@attr.s
class Message(object):
    # username = attr.ib() #  TODO in the future keep track of the users
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
