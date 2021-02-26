import hashlib
def md5encrypt( str ):
    hl = hashlib.md5()
    hl.update( str.encode(encoding='utf-8') )
    return hl.hexdigest()
