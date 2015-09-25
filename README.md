parser
======

This component parses source code, and looks for dependencies references.

[![Build Status](https://travis-ci.org/DependencyWatcher/parser.png)](https://travis-ci.org/DependencyWatcher/parser)

### Ignoring resources from beign parsed ###

The parser supports file `.dwignore`, which must be placed in the project root, and can contain a list of patterns of ignored files or directories.

Example:

    # Ignore tests folder and all of its contents:
    tests/
    # Ignore .txt files
    *.txt

