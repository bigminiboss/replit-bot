from random import choice
import uuid

_chars = "qwertyuiopasdfghjklzxcvbmmQWERTYUIOPASDFGHJKLZXCVBNM"


def random_characters(n):
    """`rand_chars + uuid.uuid4()`. uuid v4 doesn't need any inputs which is why it used"""
    output = ""
    for i in range(n):
        output += choice(_chars)
    return output + str(uuid.uuid4())
