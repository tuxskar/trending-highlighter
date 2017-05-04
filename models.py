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
        user_names = ['peter', 'jon', 'joakim', 'juan', 'pepe', 'penelope', 'maria', 'ana', 'monica']
        colors = ["rgb(247, 202, 201)", "rgb(247, 120, 107)", "rgb(145, 168, 208)", "rgb(3, 79, 132)",
                  "rgb(152, 221, 222)", "rgb(152, 150, 164)", "rgb(221, 65, 50)",
                  "rgb(177, 143, 106)", "rgb(121, 199, 83)"]
        for username, color in zip(user_names, colors):
            _users[username] = color
    return _users


RoomsCounter = dict()

SENTENCES = {
    'cats': [
        "El paraíso jamás será paraíso a no ser que mis gatos estén ahí esperándome.",
        "Dios hizo el gato para ofrecer al hombre el placer de acariciar un tigre.",
        "La elegancia quiso cuerpo y vida, por eso se transformó en gato.",
        "No hay gatos corrientes.",
        "Los gatos saben por instinto la hora exacta a la que van a despertarse sus amos, y los despiertan diez minutos\
         antes.",
        "Cualquier gato que no consigue atrapar a un ratón finge que iba tras una hoja seca.",
        "Los gatos son amos amables, mientras que recuerdes cuál es tu propio sitio.",
        "Si quieres escribir sobre seres humanos, lo mejor que puedes tener en casa es un gato.",
        "El gato es el único animal que ha logrado domesticar al hombre.",
        "El gato no nos acaricia, se acaricia con nosotros."
    ],
    'dogs': [
        "El mejor test a la hora de elegir un cachorro es mirarse honestamente en el espejo",
        "Mi meta en la vida es llegar a ser tan maravilloso como mi perro cree que soy",
        "Tú no tienes un perro, el perro te tiene a tí",
        "Los perros no son toda tu vida, pero hacen tu vida completa.",
        "Errar es de humanos, perdonar es de perros.",
        "El perro sabe, pero no sabe que sabe",
        "Dos perros pueden matar a un león",
        "El perro es el único ser que te quiere más que tú mismo.",
        "Entre más personas conozco, más quiero a mi perro.",
        "Yo amo a los perros. Ellos no hacen nada por razones políticas."
    ]
}
