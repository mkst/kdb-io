import os
import sys

# local libraries
from read import readfile, readfiles, syms

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if len(sys.argv) == 3:
      symfiles = sys.argv[2]
      for symfile in symfiles.split(","):
        syms[symfile.split("/")[-1]] = readfile(symfile)
    target = sys.argv[1]
    if (not os.path.exists(target)):
      print "error:",target,"not found"
      sys.exit(1)
    if (os.path.isdir(target)):
      files = []
      if (os.path.exists(target + "/.d")):
        files = readfile(target + "/.d")
      else:
        files = os.listdir(target)
      res = readfiles(target, files)
      keys = res.keys()
      for k in keys:
        print res[k][:10] # only print first 10 rows
    else:
      res = readfile(sys.argv[1])
      print res
  else:
    print "Usage:\n  python -m kio <kdb file or folder> [sym1,sym2,sym3]"