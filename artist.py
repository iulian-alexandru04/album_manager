import re


class Artist():
    __field = r'[\w\s]+'
    def __init__(self, name, country):
        if not re.match(Artist.__field, name):
            raise ValueError('invalid name')
        if not re.match(Artist.__field, country):
            raise ValueError('invalid country')
        self.__name = name
        self.__country = country
        self.__albums = []

    @property
    def name(self):
        return self.__name

    @property
    def country(self):
        return self.__country

    def get_albums(self):
        yield from self.__albums

    def add_album(self, new_album):
        self.__albums.append(new_album)

    def get_songs(self):
        for alb in self.__albums:
            yield from alb.songs()

    def sort_albums_by_date(self):
        self.__albums.sort(key=Album.sort_key, reverse=True)

    def __eq__(self, other):
        s = (self.__name, self.__country, self.__albums)
        o = (other.__name, other.__country, other.__albums)
        return s == o

    def __str__(self):
        header = f'{self.__name} ({self.__country})'
        body = '\n---\n'.join([str(a) for a in self.__albums])
        return f'{header}\n---Dicography---\n{body}'

    @staticmethod
    def from_string(input_str):
        pattern = r'(?P<name>' + Artist.__field + r') ' + \
                  r'\((?P<country>' + Artist.__field + r')\)' + \
                  r'\n---Dicography---\n(?P<albums>.*)'
        match = re.search(pattern, input_str, re.DOTALL)
        if not match:
            raise ValueError()
        name = match.group('name')
        country = match.group('country')
        albums = match.group('albums')
        artist = Artist(name, country)
        for a in albums.split('\n---\n'):
            if a.strip():
                artist.add_album(Album.from_string(a))
        return artist
