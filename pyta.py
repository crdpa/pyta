#!/usr/bin/env python3
#  _  _ _|  _   _
# (_ | (_| |_) (_|
#          |
# pyta.py
# ID3 tag editor

import argparse
import tempfile
import sys
from os import listdir, path, environ
from mutagen.easyid3 import EasyID3
from subprocess import call


def dir_path(dir):
    if path.isdir(dir):
        files = list_files(dir)
        return files
    else:
        raise NotADirectoryError(dir)


def list_files(dir):
    files_to_edit = []
    for f in listdir(dir):
        if path.isfile(f) and f.lower().endswith(('.mp3', '.flac', '.ogg',
                                                  '.opus')):
            files_to_edit.append(f)

    return files_to_edit


def parse_tags(file):
    tags = EasyID3(file)
    tmp = tempfile.NamedTemporaryFile(mode='w')
    for k, v in sorted(tags.items()):
        tmp.write(k + ': ' + v[0] + '\n')

    return tmp, tags


def edit_tags(tf, tags):
    EDITOR = environ.get('EDITOR', 'nano')
    tf.flush()
    call([EDITOR, tf.name])
    tf.seek(0)

    lines = []
    with open(tf.name) as f:
        lines = f.readlines()

    for line in lines:
        key = line[:line.find(':')]
        value = line[line.find(':')+2:-1]
        tags[key] = value

    tags.save()


def main():
    parser = argparse.ArgumentParser(prog='pyta.py', usage='%(prog)s file')
    parser.add_argument('--path', '-p', metavar='path to directory')
    parser.add_argument('--file', '-f', metavar='file(s)')
    args = parser.parse_args()

    if args.path:
        files = dir_path(args.path)
        for f in files:
            tmpfile, tags = parse_tags(f)
            edit_tags(tmpfile, tags)
    elif args.file:
        tmpfile, tags = parse_tags(args.file)
        edit_tags(tmpfile, tags)

    tmpfile.close()


if __name__ == "__main__":
    main()
