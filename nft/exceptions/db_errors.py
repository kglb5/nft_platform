from patreon.exception import PatreonException


class DBError(PatreonException):
    pass


class BadEnumType(DBError):
    def __init__(self, value, column_name):
        self.value = value
        self.column_name = column_name

    def __str__(self):
        return "The value {} is not allowed in the {} column".format(self.value, self.column_name)
