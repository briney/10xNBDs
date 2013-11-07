#!/usr/bin/python
# filename: batch_mongoimport.py

import os
import argparse
import subprocess

parser = argparse.ArgumentParser("Performs the mongoimport operation on all files in the input directory.  Determines the appropriate collection using the filename.")
parser.add_argument('-ip', dest='ip', default='localhost', help="The IP address of the MongoDB server. Defaults to 'localhost'.")
parser.add_argument('-port', dest='port', default=27017, type=int, help="The port used to connect to the MongoDB server. Defaults to '27017'.")
parser.add_argument('-in', dest='input_dir', required=True, help="A directory containing multiple JSON files for import to MongoDB.")
parser.add_argument('-db', dest='db', required=True, help="The MongoDB database for import.")
parser.add_argument('-log', dest='log', required=True, help="Log file for the mongoimport stdout.")
parser.add_argument('-split', dest='split', default=1, type=int, help="Builds the collection name by truncating at the <split> occurance of the <delim> character.  Default is 1.")
parser.add_argument('-delim', dest='delim', default='_', help="The character delimiter used to split the filename to get the collection name.  Default is '_'.")
parser.add_argument('-split_only', dest='split_only', default=False, action='store_true', help="Instead of truncating the filename to get the collection name, takes only the split for the collection. Default is False.")
args = parser.parse_args()


def mongo_import(json, db, coll, log):
	mongo_cmd = 'mongoimport --host {0} --port {1} --db {2} --collection {3} --file {4}'.format(args.ip, args.port, db, coll, json)
	mongo = subprocess.Popen(mongo_cmd, shell=True, stdout=log)
	mongo.communicate()

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def get_collection(i):
	delim = str(args.delim)
	if args.split_only:
		return os.path.basename(i).split(delim)[args.split - 1]
	if args.split <= 1:
		return os.path.basename(i).split(delim)[0]
	else:
		pre_collection = os.path.basename(i).split(delim)
		return delim.join(pre_collection[:args.split])

def main():
	in_files = listdir_fullpath(args.input_dir)
	log_handle = open(args.log, 'a')
	open(args.log, 'w').write('')
	for i in in_files:
		coll = get_collection(i)
		print "\nPerforming mongoimport on {0}.\nImporting the file into collection {1}.".format(os.path.basename(i), coll)
		log_handle.write('\n\n----------------------------------------\nFile: {0}\Collection: {1}\n----------------------------------------\n'.format(i, coll))
		mongo_import(i, args.db, coll, log_handle)
	print "\nDone. {0} files were imported into MongoDB.\n\n".format(len(in_files))



if __name__ == '__main__':
	main()