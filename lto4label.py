#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

from code39 import encode_39

from StringIO import StringIO

from optparse import OptionParser

import logging



log = logging.getLogger('lto4label')



class Label(object):
    
    _width = 78
    _height = 17

    _colors = {
        0:"#df4e59",
        1:"#faf029",
        2:"#bdd124",
        3:"#85c9d9",
        4:"#c8c7b9",
        5:"#de9426",
        6:"#ca739e",
        7:"#7ebf56",
        8:"#f2c23c",
        9:"#9087bb",
        }

    def __init__(self, number):
        number = int(number)
        try:
            assert 0 <= number <= 999999
        except AssertionError, e:
            log.error("%d: Number is out of range. Must be between 0 and 999999 inclusive." % number)
            sys.exit()
        self.number = number
    
    @property
    def text_number(self):
        return "%06d" % self.number
    
    @property
    def text(self):
        return "%sL4" % self.text_number
    
    @property
    def code_39(self):
        return encode_39(self.text)

    @property
    def color_numbers(self):
        c = []
        for n in self.text_number:
            n = int(n)
            c.append((n, self._colors[n]))
        return c



def mm_to_px(mm):
    return mm * 90 / 25.4



def render(width, height, margin, rows, columns, labels, legend=""):
    r = StringIO()
    r.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="%fmm"
   height="%fmm"
   version="1.1"
   style="font-family:freesans, sans">
""" % (width, height))

    x = margin
    y = margin
    while labels:
        label = labels.pop(0)
        assert x + 78 < (width - margin), "Too many for page"
        if  y + 17 > (height - margin):
            x += 78 + margin
            y = margin
        r.write("""  <g transform="translate(%f,%f)">
    <rect ry="1mm" rx="1mm" y="0" x="0" height="17mm" width="78mm" style="fill:none;stroke:black;stroke-opacity:.2;stroke-width:0.1mm;" />
    <g transform="scale(1.55,1)">
""" % (mm_to_px(x), mm_to_px(y)))

        cx = 10
        for f in label.code_39:
            if f in 'bB':
                r.write("""      <rect y="0" x="%f" height="17mm" width="%f" style="fill:black;stroke-width:0;" />
""" % (cx, 1 + 2 * int(f == "B")))
            cx += 1 + 2 * int(f in "BW") 
        r.write("""    </g>
""")

        nwidth = 10.3
        nx = 3

        for n, color in label.color_numbers:
            r.write("""    <rect y="0" x="%fmm" height="5mm" width="%fmm" style="fill:%s;stroke:#000000;stroke-width:0.1mm;" />
    <text y="3.9mm" x="%fmm" style="font-size:4mm; text-anchor: middle;">%s</text>
""" % (nx, nwidth, color, nx + nwidth / 2, n))

            nx += nwidth
        r.write("""    <rect y="0" x="%fmm" height="5mm" width="%fmm" style="fill:white;stroke:#000000;stroke-width:0.1mm;" />
    <text y="3.3mm" x="%fmm" style="font-size:2.5mm; text-anchor: middle;">L4</text>
  </g>
""".format(nx, nwidth, nx + nwidth / 2))

        y += 17 + margin

    r.write("""</svg>
""")
    
    return r.getvalue()
    
    



if __name__ == "__main__":
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.WARNING)

    usage = """Usage: %prog TAPENUMBER...

TAPENUMBER... :  Up to 20 integers between 0 and 999999 inclusive."""

    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbosity",
                      help="Print verbose information for debugging.", default=None)
    parser.add_option("-q", "--quiet", action="store_false", dest="verbosity",
                      help="Suppress warnings.", default=None)

    (options, args) = parser.parse_args()

    if options.verbosity:
        log.setLevel(logging.INFO)
    elif options.verbosity is False:
        log.setLevel(logging.ERROR)

    if not args:
        parser.print_usage()
        quit()


    width = 210.
    height = 297.
    margin = 10.
    columns = int((width - margin) / (Label._width + margin))
    rows = int((height - margin) / (Label._height + margin))

    if not columns:
        print "Too thin."
        quit()
    if not rows:
        print "Too short."
        quit()


    labels = []
    for arg in args:
        labels.append(Label(arg))

    if len(labels) > rows * columns:
        log.error("Error. Too many labels for page. Maximum is 20.")
        sys.exit()

    print render(width=width, height=height, margin=margin, rows=rows, columns=columns, labels=labels, legend="Disable 'Scale to fit page' in print options (print at '100%' size).")
