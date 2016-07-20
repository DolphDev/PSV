

def multireplace(s, *args, rw=""):
    for x in args:
        s = s.replace(x, rw)
    return s

