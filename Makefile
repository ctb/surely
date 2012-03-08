BOWTIEDIR=

all: genome.fa genome-reads.fa genome.1.ebwt

clean:
	@rm -f genome.fa genome-reads.fa genome*.ebwt

genome.fa:
	python make-random-genome.py > genome.fa

genome-reads.fa: genome.fa
	python make-reads.py genome.fa > genome-reads.fa

genome.1.ebwt: genome.fa
	$(BOWTIEDIR)bowtie-build genome.fa genome
