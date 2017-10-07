# Data representation

| Type | Description | Size | struct.unpack | Notes                              |
|:----:|:-----------:|:----:|:-------------:|:----------------------------------:|
|   1  | boolean     |   1  |     <?        | 0=False, 1=True                    |
|   2  | uuid        |  16  |     >QQ       | big-endian                         |
|   4  | byte        |   1  |     <c        |                                    |
|   5  | short       |   2  |     <h        |                                    |
|   6  | int         |   4  |     <i        |                                    |
|   7  | long        |   8  |     <q        |                                    |
|   8  | real        |   4  |     <f        |                                    |
|   9  | float       |   8  |     <d        |                                    |
|  10  | char        |   1  |     <c        |                                    |
|  11  | symbol      |   *  |     n/a       | cstring                            |
|  12  | timestamp   |   8  |     <q        | nanoseconds since 2000.01.01       |
|  13  | month       |   4  |     <i        | months since 2000.01.01            |
|  14  | date        |   4  |     <i        | days since 2000.01.01              |
|  15  | datetime    |   8  |     <d        | days since 2000.01.01 (fractional) |
|  16  | timespan    |   8  |     <q        | nanoseconds                        |
|  17  | minute      |   4  |     <i        | minutes since midnight             |
|  18  | second      |   4  |     <i        | seconds since midnight             |
|  19  | time        |   4  |     <i        | milliseconds since midnight        |

# Header

| Header             | Description | Notes |
|:------------------:|:-----------:|:-----:|
| 0xff01             | Atom        |       |
| 0xfe20             | List        |       |
| 0x6b787a6970706564 | Compressed  |       |

# Splayed database

## .d file

The `.d` file contains the names of the columns that will be read in when the base directory is loaded into a Q process.

**Hexdump of a .d file:**
```
$ xxd simple/.d
0000000: ff01 0b00 1200 0000 6100 6200 6300 6400  ........a.b.c.d.
0000010: 6500 6600 6700 6800 6900 6a00 6b00 6c00  e.f.g.h.i.j.k.l.
0000020: 6d00 6e00 6f00 7000 7100 7200            m.n.o.p.q.r.
```

**Explanation:**
```
ff01 0b00           | magic header for .d file
1200 0000           | number of columns (0x12 -> 18)
6100 6200           | variable length payload, c strings (NUL terminated)
...                 | remainder of payload
```

## Simple columns

Simple columns are lists of atoms.

**Hexdump of simple column file:**
```
$ xxd simple/a | head -3
0000000: fe20 0100 0000 0000 4042 0f00 0000 0000  . ......@B......
0000010: 0001 0000 0001 0001 0100 0100 0100 0100  ................
0000020: 0001 0001 0000 0101 0001 0000 0100 0101  ................
```

**Explanation:**
```
ff20                | magic header for splayed column
01                  | data type of column (1=boolean)
00                  | attributes (0=none, 1=sorted, 2=unique, 3=parted, 4=grouped)
0000 0000           | 4 byte padding
4042 0f00 0000 0000 | long, number of entries (cannot be trusted)
0001 0000 0001 0001 | variable length payload (in this case 1011b...)
...                 | remainder of payload
```

## Nested columns

Nested columns are lists of (potentially varying length) lists. The columns are saved into two files, one that contains the data (# file) and one that contains lengths of each list within  the data file.

### Offsets file

**Hexdump of offsets file:**
```
$ xxd nested/a | head -3
0000000: fe20 4e00 0000 0000 0a00 0000 0000 0000  . N.............
0000010: 0600 0000 0000 0000 1000 0000 0000 0000  ................
0000020: 1300 0000 0000 0000 1a00 0000 0000 0000  ................
```

**Explanation:**
After the standard header is a list of longs, each long gives the length of each list within the data file
```
fe20                | magic header for splayed column
4e00                | data type of column (78=nested boolean)
0000 0000           | 4 byte padding
0a00 0000 0000 0000 | long, number of entries (cannot be trusted)
0600 0000 0000 0000 | long, length of first list (6)
...                 | remainder of payload
```

### Data file

**Hexdump of data file:**
```
$ xxd nested/a#
0000000: 0000 0100 0100 0100 0001 0101 0101 0000  ................
0000010: 0000 0101 0101 0000 0000 0100 0100 0001  ................
0000020: 0000 0101 0001 0101 0101 0101 0001 0000  ................
...
```

## enumerated columns

## sym file

The `sym` file has a similar layout to the `.d` file, but the length field is zero.

**Hexdump of sym file:**
```
$ xxd sym
0000000: ff01 0b00 0000 0000 6100 6500 6400 6300  ........a.e.d.c.
0000010: 6200
```

**Explanation:**
The payload of the sym file is used to map back from enumerations (e.g. `0 1 2`) to the underlying values (e.g. `"a" "e" "d"`):

```
ff01 0b00           | magic header
0000 0000           | long, padding
6100 6500 6400 6300 | c string payload
...                 | remainder of payload
```

## Compressed columns

There are 4 types of compression available to kdb (as of v3.4):

 - 0, no compression
 - 1, kdb IPC
 - 2, gzip
 - 3, snappy

All compressed files have a magic header of `0x6b787a6970706564` (`kxzipped` in ASCII), the 9th byte identifies the compression used:

 - `0xfe` no compression
 - `0x01` kdb IPC compression
 - `0x78` gzip compression
 - `0x??` snappy (TBD.. `"sNaPpY"`)

The final 12 bytes of the compressed file contains the number of compressed blocks (long), along with the compression used (int).

**Example trailer:**
```
0200 0000           | 2 = gzip
0100 0000 0000 0000 | 1 = 1 block
```

There is more information stored in the trailer, but that differs based on the compression used:

### No compression

When file compression is enabled, but kdb determines that compression would not be beneficial, the columns are written down uncompressed, however they still have the `kxzipped` header and trailer.

**Header:**
```
$ xxd compressed/c | head -3
0000000: 6b78 7a69 7070 6564 fe20 0400 0000 0000  kxzipped. ......
0000010: e803 0000 0000 0000 6e04 9820 7511 ed59  ........n.. u..Y
0000020: 680d a44b e5e9 59b2 808f 908b 531f f447  h..K..Y.....S..G
```
**Trailer:**
```
$ xxd compressed/c | tail -3
0000400: 0200 0000 0206 0000 f803 0000 0000 0000  ................
0000410: 0004 0000 0000 0000 0000 0400 0000 0000  ................
0000420: f803 0000 0000 0000 0100 0000 0000 0000  ................
```

Thus to process these, the first 8 bytes can be dropped along with the trailing `(5+num_blocks)*8` bytes (as the trailer does not contain any useful information).

### Kdb IPC

TBD

### Gzip compression

The trailer contains offsets to the end of each compressed block, separated by 4-byte chunks containing the integer value `2`.

```
$ xxd compressed/a | tail -4
0003e70: e7ff fdfd 3f0b f1c4 b102 0000 0002 0600  ....?...........
0003e80: 00b0 8601 0000 0000 0079 3e00 0000 0000  .........y>.....
0003e90: 0000 0004 0000 0000 0071 3e00 0002 0000  .........q>.....
0003ea0: 0001 0000 0000 0000 00                   .........
```

**Explanation:**
```
...
fffd fd3f 0bf1 c4b1 | gzip block
0200 0000           | padding
0206 0000           | end of gzip block = 1538
b086 0100 0000 0000 | uncompressed length = 100016
793e 0000           | size of payload excluding trailer = 15993
0000 0000           | padding
0000 0400 0000 0000 | blocksize = 262144 (2**18)
713e 0000           | size of payload excluding header + trailer = 15985
0200 0000           | compression used = 2 = gzip
0100 0000 000 00000 | number of blocks = 1
```

This aligns with what `-21!` gives for the file
```
q)-21!`:compressed/a
compressedLength  | 16041
uncompressedLength| 100016
algorithm         | 2i
logicalBlockSize  | 18i
zipLevel          | 6i
```

### Snappy

TBD