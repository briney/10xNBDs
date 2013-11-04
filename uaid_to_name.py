#!/usr/bin/python
# filename: uaid_to_name.py

import os
import glob
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser("Parses through merged MiSeq reads and appends the UAID to the sequence name.")
parser.add_argument('-in', dest='input',required=True, help="The input FASTA file of UAID-barcoded sequences. If a directory is provided, all files in the directory will be iteratively processed.")
parser.add_argument('-out', dest='output', required=True, help="Directory for the output files. Required.")
parser.add_argument('-uaid', dest='uaid_length', type=int, default=20, help="Length of the UAID barcode. Default is 20.")
args = parser.parse_args()


def list_files(d):  
	return glob.glob(d + '/*')

def get_uaid(seq):
	return seq[:args.uaid_length]

def get_output_handle(f):
	o = os.path.join(args.output, os.path.basename(f))
	open(o, 'w').write('')
	return open(o, 'a')

def parse_uaids(f, out_handle):
	for seq in SeqIO.parse(open(f, 'r'), 'fasta'):
		index = get_uaid(str(seq.seq))
		seq_id = '{0}_{1}'.format(seq.id, index)
		trunc_seq = str(seq.seq)[args.uaid_length:]
		out_handle.write('>{0}\n{1}'.format(seq_id, trunc_seq))

def main():
	files = list_files(args.input)
	for f in files:
		o = get_output_handle(f)
		parse_uaids(f, o)


if __name__ == '__main__':
	main()