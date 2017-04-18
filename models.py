import datetime

import attr


@attr.s
class Message(object):
    # username = attr.ib() #  TODO in the future keep track of the users
    msg = attr.ib()
    timestamp = attr.ib(default=datetime.datetime.utcnow)
