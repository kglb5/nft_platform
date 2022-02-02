class EncryptionError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return "{} ({})".format(self.__class__.__name__, str(self.original_exception))


class InvalidPublicKey(EncryptionError):
    pass


class InvalidPrivateKey(EncryptionError):
    pass


class InvalidCryptoInput(EncryptionError):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return "{} ({})".format(self.__class__.__name__, str(self.reason))


class InvalidEncryptData(InvalidCryptoInput):
    pass


class EncryptionFailure(EncryptionError):
    pass


class InvalidDecryptData(InvalidCryptoInput):
    pass


class DecryptionFailure(EncryptionError):
    pass
