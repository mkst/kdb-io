# kdb types to python types

import uuid as u
from datetime import datetime as dt, timedelta, time as t
from dateutil.relativedelta import relativedelta

epoch = dt.fromordinal(730120)

def UUID(x):
  return [u.UUID(int=(a<<64)|b) for a,b in zip(x[0::2],x[1::2])]

def date(x):
  return [epoch+timedelta(days=a) for a in x]

def minute(x):
  return [t(a//60, a%60) for a in x]

def second(x):
  return [t(a//3600, a%3600//60, a%60) for a in x]

def time(x):
  return [t(a//3600000, a%3600000//60000, a%3600000%60000//1000, a%1000) for a in x]

def timespan(x):
  return [timedelta(microseconds=a/1000) for a in x]           # no nanosecond support in datetime

def timestamp(x):
  return [epoch+timedelta(microseconds=a/1000) for a in x]     # no nanosecond support in datetime

def datetime(x):
  return [epoch+timedelta(microseconds=a*86400000000) for a in x]

def month(x):
  return [epoch+relativedelta(months=a) for a in x]            # timedelta does not support months=