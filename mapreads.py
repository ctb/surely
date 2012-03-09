import tempfile, os, shutil
import subprocess

def get_temp_filename(filename, tempdir=None):
    if tempdir is None:
        tempdir = tempfile.mkdtemp(prefix='mapreads_')
    
    return tempdir, os.path.join(tempdir, filename)

def bowtie_map_reads(indexpath, readfile, params=[], outputfile=None):
    if outputfile is None:
        _, outputfile = get_temp_filename('out.map')
        
    cmd = 'bowtie %s %s %s %s' % (" ".join(params), indexpath, readfile,
                               outputfile)
    args = ['bowtie'] + params + [indexpath, readfile, outputfile]
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, cmd)

    return outputfile, out, err

if __name__ == '__main__':
    outfile, out, err = bowtie_map_reads('random', 'genome-reads.fa', params=['-f'])
    print err
    print 'output in:', outfile
