from string import ascii_lowercase

ascii_lowercase = (ascii_lowercase+"_")

def cleanup_name(s):
    return "".join(filter(lambda x: x in ascii_lowercase, s.lower()))

