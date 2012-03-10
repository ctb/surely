#! /usr/bin/env python
import sys
import os
import screed
import mapreads

READCHUNKSIZE=16*1024

def get_chunks(filename, n_chunks):
    filesize = os.path.getsize(filename)

    chunksize = int(filesize / float(n_chunks))

    x = []
    for i in range(0, filesize - 2*chunksize, chunksize):
        x.append((i, i + chunksize))

    i += chunksize
    if (filesize - (i + chunksize)) < int(0.2*chunksize):
        x.append((i, filesize))
    else:
        x.append((i, i + chunksize))
        x.append((i + chunksize, filesize))

    return x

class ReadlineUntil(object):
    def __init__(self, fp, until, verbose=0):
        self.fp = fp
        self.until = until
        self.verbose = verbose

    def readline(self):
        line = self.fp.readline()

        if self.fp.tell() - len(line) >= self.until and line.startswith('>'):
            if self.verbose:
                print >>sys.stderr, 'STOP AT', self.fp.tell() - len(line), \
                    self.fp.tell(), self.until, line[0]
                print >>sys.stderr, 'XX', (line,)
            return ""

        return line

def retrieve_records(filename, start, stop, verbose=0):
    fp = open(filename, 'rb')
    fp.seek(start)

    line = fp.readline()
    found = False
    while line and fp.tell() < stop:
        if verbose:
            print >>sys.stderr, (line,)
            
        if line.startswith('>'):
            found = True
            break
        line = fp.readline()

    if found:
        newfp = ReadlineUntil(fp, stop, verbose)
        if verbose:
            print >>sys.stderr, "START AT:", fp.tell() - len(line)
        
        for record in screed.fasta.fasta_iter(newfp, line=line):
            yield record
    else:
        assert 0

    fp.close()

def extract_reads_to_file(filename, start, stop):
    _, tmpfile = mapreads.get_temp_filename('readchunk.fa')
    fp = open(tmpfile, 'w')
    for data in retrieve_bytes(filename, start, stop):
        fp.write(data)
    fp.close()

    return tmpfile
    
def retrieve_bytes(filename, start, stop, verbose=0):
    if verbose:
        print >>sys.stderr, 'XXX', filename, start, stop
    fp = open(filename, 'rb')
    fp.seek(start)

    line = fp.readline()
    found = False
    while line and fp.tell() < stop:
        if verbose:
            print >>sys.stderr, (line,)
            
        if line.startswith('>'):
            found = True
            break
        line = fp.readline()

    if found:
        if verbose:
            print >>sys.stderr, start, 'READING FROM:', fp.tell() - len(line)
        yield line
        while fp.tell() + READCHUNKSIZE < stop:
            yield fp.read(READCHUNKSIZE)

        remaining = stop - fp.tell()
        data = fp.read(remaining)

        line = fp.readline()
        while line and not line.startswith('>'):
            data += line
            line = fp.readline()

        yield data

        if verbose:
            print >>sys.stderr, stop, 'READING TO:', fp.tell() - len(line)
    else:
        pass

    fp.close()

if __name__ == '__main__':
    filename = '/Users/t/dev/khmer/data/100k-filtered.fa'
    x = get_chunks(filename, 8)

    #print >>sys.stderr, x, os.path.getsize(filename)
    #for n, (start, stop) in enumerate(x):
    #    print >>sys.stderr, n, start, stop, stop - start

    if 0:
        for (start, stop) in x:
            for record in retrieve_records(filename, start, stop):
                sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))
    else:
        for (start, stop) in x:
            for data in retrieve_bytes(filename, start, stop):
                sys.stdout.write(data)

#    for record in retrieve(filename, x[-2][0], x[-2][1], verbose=1):
#         sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))    
#    for record in retrieve(filename, x[-1][0], x[-1][1], verbose=1):
#         sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))    
