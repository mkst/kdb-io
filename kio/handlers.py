from struct import unpack

#local libraries
import to

simple = {
 # atoms
   -1: lambda x: unpack("<?", x),                                               #   1,  boolean
   -2: lambda x: to.UUID(unpack(">QQ", x)),                                     #   16, GUID (big-endian)
   -4: lambda x: unpack("<c", x),                                               #   1,  byte
   -5: lambda x: unpack("<h", x),                                               #   2,  short
   -6: lambda x: unpack("<i", x),                                               #   4,  integer
   -7: lambda x: unpack("<q", x),                                               #   8,  long
   -8: lambda x: unpack("<f", x),                                               #   4,  real
   -9: lambda x: unpack("<d", x),                                               #   8,  float
  -10: lambda x: unpack("<c", x),                                               #   1,  char
  -11: lambda x: unpack("<"+str(len(x)-1)+"sx", x),                             #   *,  cstring
  -12: lambda x: to.timestamp(unpack("<q", x)),                                 #   8,  timestamp
  -13: lambda x: to.month(unpack("<i", x)),                                     #   4,  month
  -14: lambda x: to.date(unpack("<i", x)),                                      #   4,  date
  -15: lambda x: to.datetime(unpack("<d", x)),                                  #   8,  datetime
  -16: lambda x: to.timespan(unpack("<q", x)),                                  #   8,  timespan
  -17: lambda x: to.minute(unpack("<i", x)),                                    #   4,  minute
  -18: lambda x: to.second(unpack("<i", x)),                                    #   4,  second
  -19: lambda x: to.time(unpack("<i", x)),                                      #   4,  time
 # lists
   1: lambda x: unpack("<"+(len(x)/1)*"?", x),                                  #   1,  boolean
   2: lambda x: to.UUID(unpack(">"+(len(x)/16)*"QQ", x)),                       #   16, GUID (big-endian)
   4: lambda x: unpack("<"+(len(x)/1)*"c", x),                                  #   1,  byte
   5: lambda x: unpack("<"+(len(x)/2)*"h", x),                                  #   2,  short
   6: lambda x: unpack("<"+(len(x)/4)*"i", x),                                  #   4,  integer
   7: lambda x: unpack("<"+(len(x)/8)*"q", x),                                  #   8,  long
   8: lambda x: unpack("<"+(len(x)/4)*"f", x),                                  #   4,  real
   9: lambda x: unpack("<"+(len(x)/8)*"d", x),                                  #   8,  float
  10: lambda x: unpack("<"+(len(x)/1)*"c", x),                                  #   1,  char
  11: lambda x: x[5:-1].split("\x00"),                                          #   *,  cstring
  12: lambda x: to.timestamp(unpack("<"+(len(x)/8)*"q", x)),                    #   8,  timestamp
  13: lambda x: to.month(unpack("<"+(len(x)/4)*"i", x)),                        #   4,  month
  14: lambda x: to.date(unpack("<"+(len(x)/4)*"i", x)),                         #   4,  date
  15: lambda x: to.datetime(unpack("<"+(len(x)/8)*"d", x)),                     #   8,  datetime
  16: lambda x: to.timespan(unpack("<"+(len(x)/8)*"q", x)),                     #   8,  timespan
  17: lambda x: to.minute(unpack("<"+(len(x)/4)*"i", x)),                       #   4,  minute
  18: lambda x: to.second(unpack("<"+(len(x)/4)*"i", x)),                       #   4,  second
  19: lambda x: to.time(unpack("<"+(len(x)/4)*"i", x)),                         #   4,  time
  }

nested = {
  78: lambda x,y: [unpack("<"+(b-a)*"?", x[1*a:1*b]) for a,b in y],             # nested boolean
  79: lambda x,y: [to.UUID(unpack(">"+(b-a)*"QQ",x[16*a:16*b])) for a,b in y],  # nested guid
  82: lambda x,y: [unpack("<"+(b-a)*"h", x[2*a:2*b]) for a,b in y],             # nested short
  81: lambda x,y: [unpack("<"+(b-a)*"c", x[1*a:1*b]) for a,b in y],             # nested byte
  83: lambda x,y: [unpack("<"+(b-a)*"i", x[4*a:4*b]) for a,b in y],             # nested int
  84: lambda x,y: [unpack("<"+(b-a)*"q", x[8*a:8*b]) for a,b in y],             # nested long
  85: lambda x,y: [unpack("<"+(b-a)*"f", x[4*a:4*b]) for a,b in y],             # nested real
  86: lambda x,y: [unpack("<"+(b-a)*"d", x[8*a:8*b]) for a,b in y],             # nested float
  87: lambda x,y: [unpack("<"+(b-a)*"c", x[1*a:1*b]) for a,b in y],             # nested char
  89: lambda x,y: [to.timestamp(unpack("<"+(b-a)*"q", x[8*a:8*b])) for a,b in y], # nested timestamp
  90: lambda x,y: [to.month(unpack("<"+(b-a)*"i", x[4*a:4*b])) for a,b in y],   # nested month
  91: lambda x,y: [to.date(unpack("<"+(b-a)*"i", x[4*a:4*b])) for a,b in y],    # nested date
  92: lambda x,y: [to.datetime(unpack("<"+(b-a)*"d", x[8*a:8*b])) for a,b in y],# nested datetime
  93: lambda x,y: [unpack("<"+(b-a)*"q", x[8*a:8*b]) for a,b in y],             # nested timespan
  94: lambda x,y: [to.minute(unpack("<"+(b-a)*"i", x[4*a:4*b])) for a,b in y],  # nested minute
  95: lambda x,y: [to.second(unpack("<"+(b-a)*"i", x[4*a:4*b])) for a,b in y],  # nested second
  96: lambda x,y: [to.time(unpack("<"+(b-a)*"i", x[4*a:4*b])) for a,b in y],    # nested time
  }