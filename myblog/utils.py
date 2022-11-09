import os
import binascii


def random_string_generator(n):
    return binascii.hexlify(os.urandom(n)).decode()
