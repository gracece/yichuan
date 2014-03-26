#!/usr/bin/python 

fp = open("line.txt")
line = []
for line in fp:
    line = line.strip().split("#")
    data = dict()
    data['timestamp'] = line[0]
    data['line'] = line[1]
    print data

