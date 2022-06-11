from django.contrib.auth.hashers import PBKDF2PasswordHasher
from werkzeug.security import _hash_internal


class Hasher(PBKDF2PasswordHasher):
    iterations = 260000
    algorithm = "pbkdf2:sha256"

    def encode(self, password, salt, iterations=None):
        self._check_encode_args(password, salt)
        iterations = iterations or self.iterations
        hash = _hash_internal(self.algorithm, salt, password)[0]
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)