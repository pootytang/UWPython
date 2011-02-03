#!/usr/bin/python

import cgi, cgitb, json
import time

cgitb.enable()
fs = cgi.FieldStorage() #debugging

print "Content-Type: text/plain\n\n"

def response(result):
    returnVal = {}
    returnVal['time'] = time.time()
    returnVal['uwnetid'] = 'delanej'
    returnVal['result'] = result
    return json.dumps(returnVal)

if fs.keys():
    val = 0
    for key in fs.keys():
        try:
            #print json.dumps( "%s = %s" % (key, fs[key].value) )
            val += int(fs[key].value)
        except ValueError:
            print "Make sure your params are numbers"
    print response(val)    
else:
    print "you so craaazy"


