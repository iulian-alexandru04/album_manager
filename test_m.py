import pytest
from main import *


class TestSong:
    def test_invalid_init(self):
        with pytest.raises(ValueError):
            Song(1)

    def test_init_with_empty_title(self):
        with pytest.raises(ValueError):
            Song('')
        with pytest.raises(ValueError):
            Song(' ')
        with pytest.raises(ValueError):
            Song('\t')

    def test_str_conversion(self):
        s = Song('title')
        assert str(s) == 'title'

    def test_equality(self):
        assert Song('same') == Song('same')
        assert Song('same') != Song('different')


class TestAlbum:
    def test_init_with_invalid_name(self):
        with pytest.raises(ValueError):
            Album('---;;;', 2020)

    def test_title_property(self):
        album = Album('title', 2020)
        assert album.title == 'title'

    def test_empty_album(self):
        album = Album('title', 2020)
        assert list(album.songs()) == []

    def test_one_song_album(self):
        album = Album('album title', 2020)
        song = Song('song title')
        album.add(song)
        assert list(album.songs()) == [song]

    def test_more_songs_album(self):
        album = Album('album title', 2020)
        first_song = Song('first song title')
        second_song = Song('first song title')
        album.add(first_song)
        album.add(second_song)
        assert list(album.songs()) == [first_song, second_song]

    def test_equality_for_same_empty_albums(self):
        first_album = Album('album title', 2020)
        second_album = Album('album title', 2020)
        assert first_album == second_album

    def test_equality_for_different_empty_albums(self):
        first_album = Album('album title', 2020)
        second_album = Album('other album title', 2020)
        newer_album = Album('album title', 2021)
        assert first_album != second_album
        assert first_album != newer_album

    def test_equality_for_same_albums_with_songs(self):
        first_album = Album('album title', 2020)
        second_album = Album('album title', 2020)
        first_album.add(Song('same song'))
        second_album.add(Song('same song'))
        assert first_album == second_album

    def test_equality_for_different_albums_with_songs(self):
        first_album = Album('album title', 2020)
        second_album = Album('album title', 2020)
        third_album = Album('album title', 2020)
        first_album.add(Song('same song'))
        second_album.add(Song('other song'))
        third_album.add(Song('same song'))
        third_album.add(Song('other song'))
        assert first_album != second_album
        assert first_album != third_album

    def test_sort_key(self):
        first_album = Album('album title', 2020)
        newer_album = Album('album title', 2021)
        higher_album = Album('higher title', 2020)
        newer_but_lower_album = Album('aaa', 2021)
        assert Album.sort_key(first_album) < Album.sort_key(newer_album)
        assert Album.sort_key(first_album) < Album.sort_key(higher_album)
        assert Album.sort_key(first_album) < Album.sort_key(newer_but_lower_album)

    def test_to_and_from_str_empty(self):
        album = Album('album title', 2020)
        assert Album.from_string(str(album)) == album 

    def test_to_and_from_str_single_track(self):
        album = Album('album title', 2020)
        album.add(Song('song title'))
        assert Album.from_string(str(album)) == album 

    def test_to_and_from_str_multiple_tracks(self):
        album = Album('album title', 2020)
        album.add(Song('first song title'))
        album.add(Song('second song title'))
        de = Album.from_string(str(album))
        assert Album.from_string(str(album)) == album 


class TestArtist:
    def test_invalid_init(self):
        with pytest.raises(ValueError):
            Artist('artist name', '--;;')
        with pytest.raises(ValueError):
            Artist('--@@#$%artist name!!@@#{}--;;', 'country')

    def test_properties(self):
        artist = Artist('artist name', 'country')
        assert artist.name == 'artist name'
        assert artist.country == 'country'

    def test_artist_without_albums(self):
        artist = Artist('artist name', 'country')
        assert list(artist.get_albums()) == []

    def test_artist_with_single_album(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('album title', 2020))
        assert list(artist.get_albums()) == [Album('album title', 2020)]

    def test_artist_with_multiple_albums(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('first album title', 2020))
        artist.add_album(Album('second album title', 2020))
        expected_albums = [Album('first album title', 2020), Album('second album title', 2020)]
        assert list(artist.get_albums()) == expected_albums

    def test_artist_with_albums_but_no_songs(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('album title', 2020))
        assert list(artist.get_songs()) == []

    def test_artist_with_one_song(self):
        artist = Artist('artist name', 'country')
        album = Album('album title', 2020)
        album.add(Song('song title'))
        artist.add_album(album)
        assert list(artist.get_songs()) == [Song('song title')]

    def test_artists_with_multiple_songs(self):
        artist = Artist('artist name', 'country')
        first_album = Album('first album title', 2020)
        first_album.add(Song('first song title'))
        first_album.add(Song('second song title'))
        second_album = Album('second album title', 2020)
        second_album.add(Song('third song title'))
        artist.add_album(first_album)
        artist.add_album(second_album)
        expected_songs = [Song('first song title'), 
                          Song('second song title'), 
                          Song('third song title')] 
        assert list(artist.get_songs()) == expected_songs

    def test_sort_albums_by_most_recent(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('first album title', 2020))
        artist.add_album(Album('second album title', 2021))
        expected_albums = [Album('second album title', 2021), 
                           Album('first album title', 2020)]
        artist.sort_albums_by_date()
        assert list(artist.get_albums()) == expected_albums

    def test_equality_for_artists_without_albums(self):
        artist = Artist('artist name', 'country')
        assert artist == Artist('artist name', 'country')
        assert artist != Artist('other artist name', 'country')
        assert artist != Artist('artist name', 'other country')

    def test_equality_for_artist_with_albums(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('album title', 2020))
        assert artist != Artist('artist name', 'country')

    def test_to_and_from_str_without_albums(self):
        artist = Artist('artist name', 'country')
        assert Artist.from_string(str(artist)) == artist

    def test_to_and_from_str_with_albums_without_songs(self):
        artist = Artist('artist name', 'country')
        artist.add_album(Album('first album name', 2020))
        artist.add_album(Album('second album name', 2020))
        assert Artist.from_string(str(artist)) == artist

    def test_to_and_from_str_with_albums(self):
        artist = Artist('artist name', 'country')
        first_album = Album('first album title', 2020)
        first_album.add(Song('first song title'))
        first_album.add(Song('second song title'))
        second_album = Album('second album title', 2021)
        second_album.add(Song('third song title'))
        assert Artist.from_string(str(artist)) == artist

