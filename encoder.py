# encoder-decoder
# methods: rle & huffman

import argparse
import filecmp
import os
import reader

def run(filename, method, decompress):
    if filename == 'test':
        test(method)
        return

    try:
        fi = reader.Reader(filename)
        alg = __import__(method)
        if decompress:
            fo = open(filename + '.depack', 'wb')
            fo.write(alg.decode(fi))
            fo.close()
        else:
            fo = open(filename + '.pack', 'wb')
            fo.write(alg.encode(fi))
            fo.close()
        fi.close()

    except IOError as e:
       print 'Oh dear.', filename, 'not found'

def find_error(filename):
    fi1 = open(filename)
    fi2 = open(filename + '.pack.depack')
    l1 = fi1.readline()
    l2 = fi2.readline()
    i = 1
    while l1 and l2:
        if len(l1) != len(l2):
            print 'Length differs: line', i
            break
        if l1 != l2:
            for j in range(len(l1)):
                if l1[j] != l2[j]:
                    print 'Symbol differs, line {0}, symbol {1}'.format(i, j + 1)
                    break
            break
        l1 = fi1.readline()
        l2 = fi2.readline()
        i += 1

def test(method):
    def process_file(filename):
        run(filename, method, False)
        run(filename + '.pack', method, True)
        print 'Before: {0} bytes, after: {1} bytes'.format(os.stat(filename).st_size, os.stat(filename + '.pack').st_size)
        not_corrupted = filecmp.cmp(filename, filename + '.pack.depack', False)
        print 'Data was {0}corrupted'.format('not ' if not_corrupted else '')
        if not not_corrupted:
            find_error(filename)

    if method == 'huffman':
        process_file('rle_0.txt ')
        process_file('new.txt')
        process_file('sleepy_hollow.txt')
        process_file('hp.txt')

    if method == 'rle':
        for i in range(3):
            process_file('rle_{0}.txt'.format(i))

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='name of a file')
parser.add_argument('-m', '--method', help='method to be used', choices=['rle', 'huffman'], required=True)
parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')

args = parser.parse_args()
run(args.filename, args.method, args.decompress)
