from collections import namedtuple
from song import Song
from album import Album
from artist import Artist


def add_artist():
    print('-----------Add-Artist----------')
    print("artist's name: ", end='')
    name = input()
    print("artist's country: ", end='')
    country = input()
    sorted_artists.append(Artist(name, country))


def show_artist():
    print('-----------Show-Artist----------')
    print("artist's name: ", end='')
    name = input()
    for artist in sorted_artists:
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
    for artist in sorted_artists:
        if artist.name == artist_name:
            artist.add_album(album);


def add_song_to_album():
    print('----------Add-Song----------')
    print("artist's name: ", end='')
    artist_name = input()
    print("album's title: ", end='')
    title = input()
    for artist in sorted_artists:
        if artist.name == artist_name:
            for album in artist.get_albums():
                if album.title == title:
                    print('song title: ', end='')
                    album.add(Song(input()))


def sort_disks_for_all_artists():
    for artist in sorted_artists:
        artist.sort_albums_by_date()


sorted_artists = []
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
