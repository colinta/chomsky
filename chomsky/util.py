

def str_or_unicode(input):
    try:
        return str(input)
    except UnicodeEncodeError:
        return unicode(input)
