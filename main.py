import re


class Song:
    def __init__(self, title):
        if type(title) is not str:
            raise ValueError('expected string')
        title = title.strip()
        if not title:
            raise ValueError('string should not be empty')
        self.__title = title

    def __str__(self):
        return self.__title

    def __eq__(self, other):
        return self.__title == other.__title


class Album:
    __title_regex = r'[\w\s]+'
    def __init__(self, title, year):
        if not re.match(Album.__title_regex, title):
            raise ValueError('invalid title')
        self.__title = title
        self.__year = int(year)
        self.__tracks = []

    def add(self, song):
        self.__tracks.append(song)

    @property
    def title(self):
        return self.__title

    def songs(self):
        yield from self.__tracks

    def __eq__(self, other):
        s = (self.__title, self.__year, self.__tracks) 
        o = (other.__title, other.__year, other.__tracks)
        return s == o

    @staticmethod
    def sort_key(self):
        return (self.__year, self.__title)

    def __str__(self):
        header = f'{self.__title} ({self.__year})'
        body = '\n'.join(str(song) for song in self.__tracks)
        return f'{header}\n{body}'

    @staticmethod
    def from_string(input_str):
        pattern = r'(?P<title>' + Album.__title_regex + r') \((?P<year>\d+)\)\n(?P<tracks>.*)'
        match = re.search(pattern, input_str, re.DOTALL)
        if not match:
            raise ValueError()
        title = match.group('title')
        year = int(match.group('year'))
        tracks = match.group('tracks')
        album = Album(title, year)
        print(f'tracks: {tracks}')
        for t in tracks.split('\n'):
            if t.strip():
                album.add(Song(t))
        return album


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

