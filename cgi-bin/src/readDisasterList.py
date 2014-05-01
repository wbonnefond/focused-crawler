#!/usr/bin/python

print 'Content-Type: text/plain\n'
file = open('disaster-list.txt', 'r')
print file.read()
