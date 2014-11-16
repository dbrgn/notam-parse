from collections import namedtuple


Notam = namedtuple('Notam', 'intro attributes')
Intro = namedtuple('Intro', 'id operation target')
NotamID = namedtuple('NotamID', 'series number year raw')
Attribute = namedtuple('Attribute', 'type body')
