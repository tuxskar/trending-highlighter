import re
from collections import defaultdict
from random import random

from models import get_users, MessagesCollection, SENTENCES, RoomsCounter


def get_room_name(message):
    room = message.get('room', 'cats')
    if not room or room.lower() not in SENTENCES.keys():
        room = 'cats'
    return room.lower(), 'Gatos' if room == 'cats' else 'Perros'


def get_username():
    users = get_users()
    idx = int(random() * len(users)) % len(users)
    return list(users.keys())[idx]


def get_rooms(room):
    if room:
        rooms = [room]
    else:
        rooms = MessagesCollection.keys()
    return rooms


def process_word_cnts(msg, room):
    if room not in RoomsCounter:
        RoomsCounter[room] = defaultdict(int)
    for word in map(str.lower, re.split('[¿?!¡\-,\/ .\n]', msg)):
        if word:
            RoomsCounter[room][word] += 1


def get_word_counter_processed(room):
    to_ret = []
    word_counter = RoomsCounter.get(room, {})
    for k, v in word_counter.items():
        weight = v * len(k)
        title = 'Weight: {} Cnt: {}'.format(weight, v)
        to_ret.append({'text': k, 'weight': weight, 'html': {'title': title}})
    return to_ret
