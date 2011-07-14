#!/usr/bin/env python
#-*- coding: utf-8 -*-

from code39 import encode_39

from mako.template import Template

from optparse import OptionParser

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
        assert 0 <= number <= 999999
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

if __name__ == "__main__":
    usage = "Usage: %prog TAPENUMBER..."
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if not args:
        parser.print_usage()
        quit()


    width = 210
    height = 297
    margin = 10
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

    
    label_template = Template(filename="template/label.svg")
    if len(labels) > rows * columns:
        print "Too many for page"
        quit()

    print label_template.render(width=width, height=height, margin=margin, rows=rows, columns=columns, labels=labels, legend="Disable 'Scale to fit page' in print options (print at '100%' size).")
