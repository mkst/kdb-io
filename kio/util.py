import zlib
import struct
# utilities

def sums(x):
  if len(x) == 1:
    return x                                                   # nothing to sum
  else:
    return reduce(lambda a, b: a+[a[-1]+b], x, [0])[1:]        # sum over list

def decompress(data):
  assert(data[0:8] == "kxzipped")                              # sanity

  trailer = struct.unpack("<iq", data[-12:])                   # unpack last 12 bytes of data
  compression_type, num_blocks = trailer                       # 0=none, 1=kdb, 2=gzip, 3=snappy

  if compression_type == 0:                                    # no compression used
    return data[8:-((5+num_blocks)*8)]                         # trim header and trailer and return

  elif compression_type == 2:                                  # gzip/zlib compression used
    uncompressed_data = ""                                     # placeholder for uncompressed data
    offsets_block = data[-(12+8*num_blocks):-12]               # contains end of each compressed block
    offsets = struct.unpack("<"+(num_blocks)*"xxxxi", offsets_block)[:-1] # drop last offset
    zlib_offsets = sums((0,) + offsets)                        # sum up offsets to get start of each block
    for o in zlib_offsets:
       uncompressed_data += zlib.decompress(data[8+o:])        # decompress each block
    return uncompressed_data                                   # return decompressed data

  else:
    return None                                                # FIXME no handler for compression type