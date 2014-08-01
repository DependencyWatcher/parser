#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from dependencywatcher.parser.parser import Parser

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "USAGE: %s <directory>" % sys.argv[0]
		sys.exit(2)
	print Parser.parse_dir(sys.argv[1])

