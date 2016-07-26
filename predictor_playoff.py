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
  def winner(o):
    if o[0] > o[1]:
      return 0
    if o[0] < o[1]:
      return 1
    return o[3]
  e = 0
  if c[0] == c[1]:
    for o in cs:
      if o[0] == o[1]:
        if c[0] == o[0]:
          if winner(c) == winner(o):
            s = 4
          else:
            s = 3
        else:
          if winner(c) == winner(o):
            s = 3
          else:
            s = 2
      else:
        if winner(c) == winner(o):
          s = 1
        else:
          s = 0
      e += s * o[2]
    return (e, c[0], c[1], c[3])

  e = 0
  for o in cs:
    if o[0] == c[0] and o[1] == c[1]:
      s = 3
    elif c[0] - c[1] == o[0] - o[1]:
      s = 2
    elif winner(c) == winner(o):
      s = 1
    else:
      s = 0
    e += s * o[2]
  return (e, c[0], c[1])

(et, net, wr1, wet1, wk1, wr2, wet2, wk2) = \
    tuple(1 / float(p) for p in sys.stdin.next().split())

net = et + net
et /= net
nw = wr1 + wet1 + wk1 + wr2 + wet2 + wk2
wet1 /= nw
wk1 /= nw
wet2 /= nw
wk2 /= nw

ke1 = wet1 / et
kk1 = wk1 / et
ke2 = wet2 / et
kk2 = wk2 / et
kn = ke1 + kk1 + ke2 + kk2
ke1 /= kn
kk1 /= kn
ke2 /= kn
kk2 /= kn

crs = [parse(l.strip()) for l in sys.stdin if len(l.strip())]
print kk1 + kk2 + ke1 + ke2

norm = sum(c[2] for c in crs)
crs = dict(((s1, s2), c / norm) for s1, s2, c in crs)

cs = []
for s1, s2 in crs:
  if s1 == s2:
    cs.append((s1, s2, crs[(s1, s2)] * kk1, 0))
    cs.append((s1, s2, crs[(s1, s2)] * kk2, 1))
    continue
  if abs(s1 - s2) > 1:
    cs.append((s1, s2, crs[(s1, s2)]))
    continue
  if s1 > s2:
    cs.append((s1, s2, crs[(s1, s2)] + crs[(s2, s2)] * ke1))
  else:
    cs.append((s1, s2, crs[(s1, s2)] + crs[(s1, s1)] * ke2))
ncs = sum(a[2] for a in cs)
cs = [(a[0], a[1], a[2] / ncs) if len(a) == 3 else \
      (a[0], a[1], a[2] / ncs, a[3]) for a in cs]

print cs

es = sorted([estimate(c, cs) for c in cs], reverse=True)
print es

for e in es[0:10]:
  if e[1] == e[2]:
    k1 = '*' if e[3] == 0 else ''
    k2 = '*' if e[3] == 1 else ''
  else:
    k1 = k2 = ''
  print '%d%s - %d%s %f' % (e[1], k1, e[2], k2, e[0])
