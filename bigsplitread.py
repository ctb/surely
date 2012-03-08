#! /usr/bin/env python
import sys
import os
import screed

READCHUNKSIZE=16*1024

def get_chunks(filename, n_chunks):
    filesize = os.path.getsize(filename)

    chunksize = int(filesize / float(n_chunks))

    x = []
    for i in range(0, filesize - 2*chunksize, chunksize):
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

def retrieve(filename, start, stop, verbose=0):
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

if __name__ == '__main__':
    filename = '/Users/t/dev/khmer/data/100k-filtered.fa'
    x = get_chunks(filename, 8)

    print >>sys.stderr, x, os.path.getsize(filename)

    for (start, stop) in x:
        for record in retrieve(filename, start, stop):
            sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))

#    for record in retrieve(filename, x[-2][0], x[-2][1], verbose=1):
#         sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))    
#    for record in retrieve(filename, x[-1][0], x[-1][1], verbose=1):
#         sys.stdout.write('>%s\n%s\n' % (record.name, record.sequence))    
