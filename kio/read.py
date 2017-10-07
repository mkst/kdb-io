import struct

# local
import util
import handlers

syms = {} # dictionary of sym files

def readfiles(basedir, files):
  t = {}
  for f in files:
    t[f] = readfile(basedir + "/" + f)
  return t

def readfile(path):
  with open(path) as f:
    return readdata(path, f.read())

def readdata(filename, data):
  header = data[0:2]
  datatype = struct.unpack("<b", data[2])[0]
  if (header == "kx"):
    return readdata(filename, util.decompress(data))
  if (datatype < 20):
    if (header == "\xfe\x20"):
      return handlers.simple[datatype](data[16:])
    elif (header == "\xff\01"):
      return handlers.simple[datatype](data[3:])
  if (datatype > 77) and (datatype < 97):
    if (header == "\xfe\x20"):
      offsets = (0,)+handlers.simple[7](data[16:])
      return handlers.nested[datatype](readfile(filename+"#"), zip(offsets, offsets[1:]))
  if filename.endswith("#"):
    return data
  if (header[0] == "\xfe"):                                  # enumerated file
    nul = data.find("\x00")                                  # first occurance of 0x00
    sym = data[1:nul]                                        # sym filename
    offset = 16 + (8 * ((nul-3) // 8))                       # length offset (16 + 8 byte alignment)
    payload = data[offset+8:]                                # drop header
    enums = struct.unpack("<"+(len(payload)/4)*"i", payload) # extract enumerations
    if sym in syms.keys():
      return [syms[sym][x] for x in enums]                   # unenumerate if symfile is loaded
    else:
      return enums                                           # otherwise return enumerations

  return None