#!/usr/bin/env python2.7

import argparse
import boto
import logging
import os
import sys

parser = argparse.ArgumentParser(
    description='Upload files from a folder to an Amazon S3 bucket')

parser.add_argument('folders', metavar='N', type=str, nargs='+',
                    help='folders containing files to be uplaoded')
parser.add_argument('-D', '--delete', action='store_true',
                    help='delete files after uploading')
parser.add_argument('-v', '--verbosity', action='count',
                    help='delete files after uploading')
parser.add_argument('-b', '--bucket',  type=str)

args = vars(parser.parse_args())
logger = logging.getLogger(__name__)

def validate_folder_paths(folder_names):
    for folder_path in folder_names:
        if not os.path.exists(folder_path):
            print '"{0}" does not exist'.format(folder_path)
            sys.exit(1)

def upload_file(bucket, file_name, folder_name, folder_path, delete=False):
    if not folder_name.endswith('/'):
        folder_name = folder_name + '/'
    key = bucket.new_key(folder_name + file_name)
    file_path = folder_path + '/' + file_name
    key.set_contents_from_filename(file_path)
    logger.debug('File {0} uploaded.'.format(folder_name + file_name))
    if delete:
        os.remove(file_path)
        logger.debug('File {0} deleted.'.format(folder_name + file_name))

def upload_folder(bucket, folder_name, delete=False):
    folder_path = os.path.abspath(
        os.path.expandvars(
            os.path.expanduser(folder_name)))
    folder_name = os.path.split(folder_path)[-1] + '/'
    folder_key = bucket.get_key(folder_name)
    if not folder_key:
        bucket.new_key(folder_name)
    files = [f for f in os.listdir(folder_path)
             if not f.startswith('.') and os.path.isfile(folder_path + '/' + f)]
    for file_name in files:
        upload_file(bucket, file_name, folder_name, folder_path, delete=delete)
    logger.info('Folder {0} uploaded'.format(folder_name))

def set_logger(verbosity_level):
    if verbosity_level == 1:
        level = logging.INFO
    elif verbosity_level >= 2:
        level = logging.DEBUG
    else:
        level = None
    logger.setLevel(level)
    logging.basicConfig(format='%(asctime)s %(message)s')

def make_s3_connection():
    return boto.connect_s3()

def main():
    set_logger(args['verbosity'])
    s3 = make_s3_connection()
    bucket_name = args['bucket']
    bucket = s3.get_bucket(bucket_name)
    validate_folder_paths(args['folders'])

    for folder_path in args['folders']:
        upload_folder(bucket, folder_path, delete=args['delete'])

if __name__ == '__main__':
    main()
