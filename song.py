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
