#!/usr/bin/python
# filename: batch_pandaseq.py

import os
import glob
import argparse
import subprocess as sp
from multiprocessing import cpu_count

parser = argparse.ArgumentParser("Parses through merged MiSeq reads and appends the UAID to the sequence name.")
parser.add_argument('-in', dest='input',required=True, help="Input directory of unmerged MiSeq reads. Should be in FASTQ format. Required.")
parser.add_argument('-out', dest='output', required=True, help="Directory for the output files. Required.")
args = parser.parse_args()


def list_files(d):  
	return glob.glob(d + '/*')


def pair_files(files):
	pairs = {}
	for f in files:
		f_prefix = '_'.join(os.path.basename(f).split('_')[:2])
		if f_prefix in pairs:
			pairs[f_prefix].append(f)
		else:
			pairs[f_prefix] = [f,]
	return pairs


def batch_pandaseq(f, r, o):
	cmd = 'pandaseq -f {0} -r {1} -d rbfkms -T {3} -w {2}'.format(f, r, o, cpu_count())
	sp.Popen(cmd, shell=True, stderr=sp.STDOUT, stdout=sp.PIPE).communicate()


def merge_reads(files):
	files.sort()
	f = files[0]
	r = files[1]
	sample = os.path.basename(f).split('_')[0]
	print_sample_info(sample)
	o = os.path.join(args.output, '{}.fasta'.format(sample))
	batch_pandaseq(f, r, o)
	print_sample_end()


def print_input_info(files):
	print '\n\nProcessing a directory of {} files\n\n'.format(len(files))

def print_sample_info(sample):
	print 'Processing sample {}...'.format(sample)

def print_sample_end():
	print 'Done.\n'


def main():
	files = list_files(args.input)
	print_input_info(files)
	pairs = pair_files(files)
	for pair in pairs:
		if len(pairs[pair]) == 2: 
			merge_reads(pairs[pair])

	

if __name__ == '__main__':
	main()
