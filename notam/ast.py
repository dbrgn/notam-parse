from collections import namedtuple


Notam = namedtuple('Notam', 'intro attributes')
Intro = namedtuple('Intro', 'id operation target')
Attribute = namedtuple('Attribute', 'type body')
