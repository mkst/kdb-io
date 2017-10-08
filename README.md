# kdb-io

A WIP python library that allows reading of _some_ q/kdb+ files into native Python datatypes.

## Howto

Generate example data:
```
$ q32 test/generate.q
KDB+ 3.5 2017.09.06 Copyright (C) 1993-2017 Kx Systems
l32/ 4()core 3635MB mark carbon 127.0.1.1 NONEXPIRE  

writing down atoms
writing down lists
writing down mixed lists
writing down simple
writing down nested
writing down compressed
```
Read some data:
```
$ python -m kio data/atoms/m
[datetime.datetime(2017, 10, 7, 0, 0)]
```
Read within python terminal:
```
>>> import kio
>>> files = kio.readfile("data/simple/.d")
>>> files
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']
>>> tab = kio.readfiles("data/simple", files)
>>> tab.keys()
['a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 'r']
>>> len(tab["a"])
100000
>>> tab["a"][0]
True
```

## Status

**Reading (WIP)**
 - [x] Atoms, e.g. `8i`
 - [x] Simple Lists, e.g. `1 2 3 4`
 - [x] Mixed Lists, e.g. `("abc";1 2 3h;1i)`
 - [x] Splayed columns
 - [x] GZIP compressed files
 - [ ] KDB compressed files
 - [ ] Snappy compressed files

**Writing (N/A)**
 - [ ] Atoms, e.g. `8i`
 - [ ] Simple Lists, e.g. `1 2 3 4`
 - [ ] Mixed Lists, e.g. `("abc";1 2 3h;1i)`
 - [ ] Splayed columns
 - [ ] GZIP compressed files
 - [ ] KDB compressed files
 - [ ] Snappy compressed files

**Other**
 - [ ] Conversion to numpy datatypes rather than native Python

## Prerequisites ##

    python-dateutil for dateutil.relativedelta
