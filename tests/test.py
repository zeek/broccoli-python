#! /usr/bin/env python

import time as Time

from broccoli import *

# Don't mind repr() for floats, since that may be shorter as of Python 2.7.
# Since the time argument might be derived from the the current time, normalize
# the display precision (e.g. prevent a rounding from tripping up a diff
# canonifier's regex).
@event
def test2(a,b,c,d,e,f,g,h,i,j,i6,j6):
    global recv
    recv += 1
    print "==== atomic a %d ====" % recv
    print repr(a), a
    print repr(b), b
    print "%.4f" % c
    print d
    print repr(e), e
    print f
    print repr(g), g
    print repr(h), h
    print repr(i), i
    print repr(j), j
    print repr(i6), i6
    print repr(j6), j6

# Same as test2 except with typing this time.
# For floating point types that are wrapped in a class, we do want to print
# repr() to see that the event typing works.  Again the time argument is
# normalized to a constant precision.
@event(int,count,time,interval,bool,double,addr,port,addr,subnet,addr,subnet)
def test2b(a,b,c,d,e,f,g,h,i,j,i6,j6):
    print "==== atomic b %d ====" % recv
    print repr(a), a
    print repr(b), b
    print repr(c), "%.4f" % c.val
    print repr(d), d
    print repr(e), e
    print f
    print repr(g), g
    print repr(h), h
    print repr(i), i
    print repr(j), j
    print repr(i6), i6
    print repr(j6), j6

rec = record_type("a", "b")
other_rec = record_type("a")

@event(rec)
def test4(r):
    global recv
    recv += 1
    print "==== record %d ====" % recv
    print repr(r)
    print repr(r.a), r.a
    print repr(r.b), r.b

bc = Connection("127.0.0.1:47758")

bc.send("test1",
    int(-10),
    count(2),
    time(current_time()),
    interval(120),
    bool(False),
    double(1.5),
    string("Servus"),
    port("5555/tcp"),
    addr("6.7.6.5"),
    subnet("192.168.0.0/16"),
    addr("2001:db8:85a3::8a2e:370:7334"),
    subnet("2001:db8:85a3::/48")
    )

recv = 0
while True:
    bc.processInput();
    if recv == 2:
        break
    Time.sleep(1)


r = record(rec)
r.a = 42;
r.b = addr("6.6.7.7")

bc.send("test3", r)

recv = 0
while True:
    bc.processInput();
    if recv == 2:
        break
    Time.sleep(1)

opt_record = record_type("one", "a", "b", "c", "d")
r = record(opt_record)
r.a = 13
r.c = "helloworld"

bc.send("test5", r)
