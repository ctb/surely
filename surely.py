import urlparse, urllib, shutil, tempfile, os
import os.path

class SchemeNotSupported(Exception):
    pass

def get_temp_filename(filename, tempdir=None):
    if tempdir is None:
        tempdir = tempfile.mkdtemp(prefix='surely_')
    
    return tempdir, os.path.join(tempdir, filename)

def acquire(url):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)

    if not scheme or scheme == 'file':
        return path
    elif scheme == 'http' or scheme == 'ftp':
        filename, _ = urllib.urlretrieve(url)
        endfile = os.path.basename(path)
        if not endfile:
            endfile = 'index'
        _, newfilename = get_temp_filename(endfile)
        shutil.move(filename, newfilename)
        return newfilename

    raise SchemeNotSupported(url)

if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    print acquire(url)
