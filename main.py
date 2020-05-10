from collections import namedtuple
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


def add_artist():
    print('-----------Add-Artist----------')
    print("artist's name: ", end='')
    name = input()
    print("artist's country: ", end='')
    country = input()
    sored_artists.append(Artist(name, country))


def show_artist():
    print('-----------Show-Artist----------')
    print("artist's name: ", end='')
    name = input()
    for artist in sored_artists:
        if artist.name == name:
            print(artist)
            return
    print('Artist not found')


def add_album_to_artist():
    print('----------Add-Album----------')
    print("artist's name: ", end='')
    artist_name = input()
    print("album's title: ", end='')
    title = input()
    print("album's year: ", end='')
    year = input()
    print("number of tracks: ", end='')
    no_tracks = int(input())

    album = Album(title, year)
    for _ in range(no_tracks):
        print('song title: ', end='')
        album.add(Song(input()))
    for artist in sored_artists:
        if artist.name == artist_name:
            artist.add_album(album);


def add_song_to_album():
    print('----------Add-Song----------')
    print("artist's name: ", end='')
    artist_name = input()
    print("album's title: ", end='')
    title = input()
    for artist in sored_artists:
        if artist.name == artist_name:
            for album in artist.get_albums():
                if album.title == title:
                    print('song title: ', end='')
                    album.add(Song(input()))


def sort_disks_for_all_artists():
    for artist in sored_artists:
        artist.sort_albums_by_date()


sored_artists = []
def main():
    Option = namedtuple('Option', 'handler, description')
    options = [Option(add_artist, 'Add artist'),
               Option(show_artist, 'Show artist'),
               Option(add_album_to_artist, 'Add album for artist'),
               Option(add_song_to_album, 'Add song to album'),
               Option(sort_disks_for_all_artists, 'Sort all albums')]
    no_options = len(options)
    while True:
        print('----------MainMenu----------')
        for num, opt in enumerate(options):
            print(f'{num + 1}.{opt.description}')
        print(f'{no_options + 1}.Exit')
        print('\nYour option: ', end='')

        choise = int(input())
        if choise <= no_options:
            options[choise - 1].handler()
        elif choise == no_options + 1:
            return
        else:
            print('You have selected an invalid option!', 'Try again!', sep='\n')


if __name__ == '__main__':
    main()

