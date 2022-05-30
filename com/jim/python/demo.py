import csv
import glob
import gzip
import json
import os
import pickle
import sys
import tempfile
from collections import deque, Iterable, namedtuple
from fnmatch import fnmatch
from itertools import dropwhile, islice, combinations, permutations, zip_longest, chain
import urllib.request

import io

import mmap

import time
from pprint import pprint
from tempfile import TemporaryFile, NamedTemporaryFile

import math


def manual_iter0(fil_name):
    with open(fil_name) as f:
        try:
            while True:
                read_line = next(f)
                print(read_line, end=' ')
        except StopIteration:
            pass
    print('\n')


def manual_iter1(file_name):
    with open(file_name) as f:
        for read_line in islice(f, 0, None):
            print(read_line, end=' ')
    print('\n')


def iter_next(item_list):
    it = iter(item_list)
    while True:
        item = next(it, None)
        if item is None:
            break
        else:
            print(item, end=' ')
    print('\n')


def yeild_frange(start, stop, increment):
    yield_iter = frange_wrap(start, stop, increment);
    while True:
        yield_item = next(yield_iter, None)
        if yield_item is None:
            break
        else:
            print(yield_item, end=' ')
    print('\n')


def frange_wrap(start, stop, increment):
    yield from frange(start, stop, increment)


def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x, ignore_types)
        else:
            yield x


def red_info_buff(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, "rb") as f:
        f.readinto(buf)
    return buf


def write_info_buff(filename, buf):
    with open(filename, 'wb') as f:
        f.write(buf)


def memory_mmap(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)


# print(sys.platform)
# print(2 ** 8)
# x = 'Jim '
# print(x * 3)
# manual_iter0('text.txt')
# manual_iter1('text.txt')
# iter_next(range(2, 10))
# yeild_frange(0, 5, 0.5)
# for read_line in reversed(list(open('text.txt'))):
#     print(read_line, end='')

f = open('text.txt')
# for line in dropwhile(lambda line: line.startswith("#"), f):
#     print(line, end='')

# items = ['a', 'b', 'c']
# for p in permutations(items, 3):
#     print(p, end=' ')
# for num, item in enumerate(items):
#     print('num={}, item={}'.format(num, item))
# print(items)

# numbers = [1, 2, 3, 4]
# characters = ['a', 'b', 'c']
# print(list(zip_longest(numbers, characters)))
# print(list(zip(numbers, characters)))
# print(list(chain(numbers, characters)))
#
# items = [1, 2, [3, 4, [5, 6], 7], 8]
# for x in flatten(items):
#     print(x)

# for chunk in iter(lambda: f.read(10), ''):
#     n = sys.stdout.write(chunk)
#     sys.stdout.flush()

# s = io.StringIO()
# s.write('hello world!')
# print('nice to meet you', file=s)
# sys.stdout.write(s.getvalue())

# with gzip.open('text.gz', 'wt', compresslevel=5) as f:
#     f.write('gzip')
# with gzip.open('text.gz', 'rt') as f:
#     print(f.read())

# bin_filename = 'sample.bin'
# with open(bin_filename, 'wb') as f:
#     f.write(b'hello world~')
# buf = red_info_buff(bin_filename)
# buf[0:5] = b'Hallo'
# write_info_buff(bin_filename, buf)

mmap_filename = 'sample.mmap'
with open(mmap_filename, 'rb') as f:
    print('rb: ', f)
with open(mmap_filename, 'w') as f:
    print('w: ', f)
    print('w.buffer: ', f.buffer)
    print('w.buffer.raw: ', f.buffer.raw)
with open(mmap_filename, 'wb') as f:
    f.seek(1000 - 1)
    f.write(b'\x00')
    print('wb: ', f)
m = memory_mmap(mmap_filename)
print('length={}, data={}', len(m), m[0:10])
m[0:11] = b'Hello World'
m.close()

print(time.ctime(os.path.getmtime(mmap_filename)))
dir_name = '/'
print([name for name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, name))])
print([name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name))])
print([name for name in os.listdir(dir_name) if fnmatch(name, '*.*')])
file_metadata = [(name, os.stat(name)) for name in glob.glob('*.*')]
for name, meta in file_metadata:
    print('file=', name, ', meta=', meta)


u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
print(f.read(15))
f.close()

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii', errors='xmlcharrefreplace')
# sys.stdout.write('Jalape\u00f1o\n')
# sys.stdout.flush()
# sys.stdout.buffer.write(b'Hello\n')


with TemporaryFile('w+b') as  f:
    f.write(b'hello world')
    f.seek(0)
    print('filename is:', f.name, ', data=', f.read())
with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)
with NamedTemporaryFile('w+t', prefix='mytemp', suffix='.txt', dir='/') as f:
    print('filename is:', f.name)

dump_file = 'sample.dump'
with open(dump_file, 'wb') as f:
    pickle.dump([1, 2, 3], f)
    pickle.dump('hello', f)
    pickle.dump({'Apple', 'Banana', 'Orange', 'Pear'}, f)

with open(dump_file, 'rb') as  f:
    print(pickle.load(f))
    print(pickle.load(f))
    print(pickle.load(f))

file_csv = 'sample.csv'
with open(file_csv) as f:
    d_csv = csv.DictReader(f)
    for d in d_csv:
        print(d)

with open(file_csv) as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    sample = namedtuple("sample", headings)
    for r in f_csv:
        row = sample(*r)
        print(row.物品ID, ' ', row)

file_json = 'sample.json'
with open(file_json, 'w') as f:
    with open(file_csv) as df:
        d_csv = csv.DictReader(df)
        data_list = []
        for d in d_csv:
            data_list.append(d)
        json.dump(data_list, f)

file_json = 'sample.json'
with open(file_json, 'r') as f:
    data_list = json.load(f, strict=False)
    for data in data_list:
        print(data)

for p in permutations(['1', '0', '1']):
    print(p)











