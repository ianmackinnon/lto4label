#!/usr/bin/env python
#-*- coding: utf-8 -*-

from StringIO import StringIO

_code_39 = {
    "0":"bwbWBwBwb",
    "1":"BwbWbwbwB",
    "2":"bwBWbwbwB",
    "3":"BwBWbwbwb",
    "4":"bwbWBwbwB",
    "5":"BwbWBwbwb",
    "6":"bwBWBwbwb",
    "7":"bwbWbwBwB",
    "8":"BwbWbwBwb",
    "9":"bwBWbwBwb",
    "A":"BwbwbWbwB",
    "B":"bwBwbWbwB",
    "C":"BwBwbWbwb",
    "D":"bwbwBWbwB",
    "E":"BwbwBWbwb",
    "F":"bwBwBWbwb",
    "G":"bwbwbWBwB",
    "H":"BwbwbWBwb",
    "I":"bwBwbWBwb",
    "J":"bwbwBWBwb",
    "K":"BwbwbwbWB",
    "L":"bwBwbwbWB",
    "M":"BwBwbwbWb",
    "N":"bwbwBwbWB",
    "O":"BwbwBwbWb",
    "P":"bwBwBwbWb",
    "Q":"bwbwbwBWB",
    "R":"BwbwbwBWb",
    "S":"bwBwbwBWb",
    "T":"bwbwBwBWb",
    "U":"BWbwbwbwB",
    "V":"bWBwbwbwB",
    "W":"BWBwbwbwb",
    "X":"bWbwBwbwB",
    "Y":"BWbwBwbwb",
    "Z":"bWBwBwbwb",
    "-":"bWbwbwBwB",
    ".":"BWbwbwBwb",
    " ":"bWBwbwBwb",
    "$":"bWbWbWbwb",
    "/":"bWbWbwbWb",
    "+":"bWbwbWbWb",
    "%":"bwbWbWbWb",
    "*":"bWbwBwBwb",
}

def encode_39(text):
    assert not "*" in text
    
    b = StringIO()
    
    b.write(_code_39["*"])
    
    for c in text:
        b.write('w')
        b.write(_code_39[c])

    b.write('w')
    b.write(_code_39["*"])
        
    return b.getvalue()
