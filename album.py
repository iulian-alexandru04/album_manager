import re
from song import Song


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
