# -*- coding: utf-8 -*-

import sys
import re

def parse(r):
  m = re.match(r'^([0-9])-([0-9])([1-9][0-9]*)/([1-9][0-9]*)$', r)
  if m:
    return (int(m.group(1)), int(m.group(2)), float(m.group(4)) / float(m.group(3)))
  m = re.match(r'^([0-9])-([0-9])([1-9][0-9]*\.[0-9]*)$', r)
  if m:
    return (int(m.group(1)), int(m.group(2)), 1/float(m.group(3)))
  raise Exception('Unexpected record %s' % r)

def estimate(c, cs):
  def res(a, b):
    return 1 if a > b else -1 if a < b else 0

  diff = c[0] - c[1]
  r = res(c[0], c[1])
  e = 0
  for o in cs:
    if o[0] == c[0] and o[1] == c[1]:
      s = 3
    elif diff == o[0] - o[1]:
      s = 2
    elif r == res(o[0], o[1]):
      s = 1
    else:
      s = 0
    e += s * o[2]
  return (e, c[0], c[1])

cs = [parse(l.strip()) for l in sys.stdin if len(l.strip())]
norm = sum(c[2] for c in cs)
cs = [(s1, s2, c / norm) for s1, s2, c in cs]
print cs
print "1: ", sum(c[2] for c in cs if c[0] > c[1])
print "D: ", sum(c[2] for c in cs if c[0] == c[1])
print "2: ", sum(c[2] for c in cs if c[0] < c[1])

es = sorted([estimate(c, cs) for c in cs], reverse=True)

for e in es[0:5]:
  print '%d - %d %f' % (e[1], e[2], e[0])

