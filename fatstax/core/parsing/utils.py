from string import ascii_lowercase, digits

ascii_lowercase = (ascii_lowercase+"_"+digits)

def cleanup_name(s):
    return "".join(filter(lambda x: x in ascii_lowercase, s.lower()))

