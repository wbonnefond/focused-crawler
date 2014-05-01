#!/usr/bin/python
import os
f = os.open('pleasecreateme.txt', os.O_CREAT|os.O_RDWR)
os.write(f, 'please work?')
os.close(f)

print 'Content-Type: text/plain\n\n'
print 'sup bro\n'
