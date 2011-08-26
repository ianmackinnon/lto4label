$SHELL := /bin/bash

all:
	echo "Nothing to do for 'all'"

test-pdf: /tmp/lto4.pdf test/lto4.pdf lto4label
	./lto4label 0 1 23 456 789 1011 12131 415161 718192 021222 324252 627282 930313 233343 536373 839404 142434 546474 849505 999999 /tmp/lto4.pdf
	cmp /tmp/lto4.pdf test/lto4.pdf

test-svg: /tmp/lto4.svg test/lto4.svg lto4labelsvg.py
	-./lto4labelsvg.py -- -1
	-./lto4labelsvg.py -- 1000000
	-./lto4labelsvg.py -- 0 1 23 456 789 1011 12131 415161 718192 021222 324252 627282 930313 233343 536373 839404 142434 546474 849505 152535 999999 > /tmp/lto4.svg
	./lto4labelsvg.py -- 0 1 23 456 789 1011 12131 415161 718192 021222 324252 627282 930313 233343 536373 839404 142434 546474 849505 999999 > /tmp/lto4.svg
	diff /tmp/lto4.svg test/lto4.svg
