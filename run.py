#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from dependencywatcher.parser.parser import Parser

import logging
logging.basicConfig(level=logging.DEBUG)

files = [
	"/home/michael/.m2/repository/org/log4mongo/log4mongo-java/0.7.4/log4mongo-java-0.7.4.jar",
	"/home/michael/Dev/projects/sci-2.0.git/legacy/poller/pom.xml",
	"/home/michael/Dev/projects/tldr.es/tldr/templates/base.html"
]

for f in files:
	for p in Parser.get_parsers(f):
			deps = p.parse()
			if len(deps) > 0:
				print "%s\n\n" % deps

