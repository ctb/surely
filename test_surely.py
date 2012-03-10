import surely
import urlparse, urllib
import os, tempfile

def get_temp_filename(filename, tempdir=None):
    if tempdir is None:
        tempdir = tempfile.mkdtemp(prefix='mapreads_')
    
    return tempdir, os.path.join(tempdir, filename)

def test_simple_file():
    _, filename = get_temp_filename('foo.txt', tempdir='/tmp')

    fp = open(filename, 'w')
    fp.write('foo')
    fp.close()

    url = urlparse.urlunparse(('file', '', filename, '', '', ''))
    gotfile = surely.acquire(filename)
    assert filename == gotfile, (filename, gotfile)

def test_simple_http():
    gotfile = surely.acquire('http://localhost/~t/ged/') # laptop

    data = open(gotfile).read()
    assert 'Lab of Genomics, Evolution, and Development' in data
