
@load frameworks/communication/listen
redef Communication::listen_port = 47758/tcp;

redef Communication::nodes += {
	["broping"] = [$host = 127.0.0.1, $events = /test1|test3|test5/, $connect=F, $ssl=F]
};


### Testing atomic types.

type foo: enum { CONST1, CONST2, CONST3 };

# No enum currently as Broccoli has trouble receiving them.
global test2: event(a: int, b: count, c: time, d: interval, e: bool, f: double, g: string, h: port, i: addr, j: subnet, i6: addr, j6: subnet);
global test2b: event(a: int, b: count, c: time, d: interval, e: bool, f: double, g: string, h: port, i: addr, j: subnet, i6: addr, j6: subnet);

event test1(a: int, b: count, c: time, d: interval, e: bool, f: double, g: string, h: port, i: addr, j: subnet, i6: addr, j6: subnet)
{
    print "==== atomic";
    print a;
    print b;
    print c;
    print d;
    print e;
    print f;
    print g;
    print h;
    print i;
    print i6;
    print j;
    print j6;
    
    event test2(-4, 42, current_time(), 1min, T, 3.14, "Hurz", 12345/udp, 1.2.3.4, 22.33.44.0/24, [2607:f8b0:4009:802::1014], [2607:f8b0:4009:802::1014]/32);
    event test2(a,b,c,d,e,f,g,h,i,j,i6,j6);
    event test2b(a,b,c,d,e,f,g,h,i,j,i6,j6);
}

### Testing record types.

type rec: record {
    a: int;
    b: addr;
};

global test4: event(r: rec);

event test3(r: rec)
{
    print "==== record";
    print r;
    print r$a, r$b;
    event test4(r);
    
    local r2 : rec;
    r2$a = 99;
    r2$b = 3.4.5.1;
    event test4(r2);
}

type opt_rec: record {
    one: int &optional;
    a: int &optional;
    b: addr &optional;
    c: string &optional;
    d: string &optional;
};

event test5(r: opt_rec)
{
    print "==== coerced record";
    print r;
    if ( r?$one ) print r$one;
    if ( r?$a ) print r$a;
    if ( r?$b ) print r$b;
    if ( r?$c ) print r$c;
    if ( r?$d ) print r$d;
}
