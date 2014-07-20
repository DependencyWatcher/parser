#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from dependencywatcher.parser.parser import Parser

import logging
logging.basicConfig(level=logging.DEBUG)

for p in Parser.get_parsers("/home/michael/Dev/projects/sci-2.0.git/legacy/poller/pom.xml"):
		print p.parse()

