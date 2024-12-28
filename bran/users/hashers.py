from django.contrib.auth.hashers import PBKDF2PasswordHasher
import hashlib


class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
        return super().encode(sha1_hash, salt, iterations)

    def encode(self, password, salt, iterations=None):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest()
        return self.encode_sha1_hash(sha1_hash, salt, iterations)
