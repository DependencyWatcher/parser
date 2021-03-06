import re, os, logging, scandir, fnmatch
from multiprocessing.pool import ThreadPool
from pkg_resources import parse_version

logger = logging.getLogger(__name__)

class FileSource(object):
    def __init__(self, filename, content=None):
        self.filename = filename
        self.content = content

    def get_name(self):
        """ Returns base name of the source file """
        try:
            return self.basename
        except AttributeError:
            self.basename = os.path.basename(self.filename)
        return self.basename

    def get_content(self):
        if self.content is None:
            with open(self.filename) as f:
                self.content = f.read()
        return self.content


class Parser(object):
    parsers = {}
    concurrency = 2

    def __init__(self, source):
        self.source = source

    def parse(self, dependencies):
        """ Returns list of dependencies required by this file """
        raise NotImplementedError

    @staticmethod
    def register_parser(patterns, parser):
        """ Registers new parser for the given set of file patterns """
        for p in patterns:
            try:
                Parser.parsers[p].append(parser)
            except KeyError:
                Parser.parsers[p] = [parser]

    @staticmethod
    def get_parsers(filename):
        """ Returns all compatible parsers for the given filename """
        source = FileSource(filename)
        for pattern, parser_classes in Parser.parsers.iteritems():
            if re.match(pattern, source.get_name(), re.I):
                for parser_class in parser_classes:
                    try:
                        yield parser_class(source)
                    except Exception as e:
                        logger.exception(e)
                        logger.warning("[%s] can't parse file: %s" % (parser_class.__name__, filename))

    @staticmethod
    def get_max_version(version_specifiers):
        """ Chooses max version defined in version specifiers list.
            For instance, if the list contains: [('>=', '1.6'), ('<', '1.8')]
            then max version will be: 1.8
        """
        max_version = None
        max_version_parsed = None
        for specifier in version_specifiers:
            op = specifier[0]
            version = specifier[1]
            version_parsed = parse_version(version)
            if op in ["==", "===", "<=", "<"]:
                if not max_version_parsed or max_version_parsed and version_parsed > max_version_parsed:
                    max_version = version
                    max_version_parsed = version_parsed
        return max_version

    @staticmethod
    def load_ignores(dir):
        ignorefile = os.path.join(dir, ".dwignore")
        ignores = []
        if os.path.exists(ignorefile):
            with open(ignorefile, "r") as f:
                for line in f:
                    line = re.sub(r"#.*", "", line).strip()
                    if (len(line) > 0):
                        ignores.append(line)
        return ignores

    @staticmethod
    def parse_file(file):
        dependencies = []
        for p in Parser.get_parsers(file):
            try:
                p.parse(dependencies)
                for d in dependencies:
                    if not "file" in d:
                        d["file"] = file
            except Exception as e:
                logger.exception(e)
                logger.warning("[%s] can't parse file: %s" % (p.__class__.__name__, file))
        return dependencies

    @staticmethod
    def parse_dir(dir): 
        ignores = Parser.load_ignores(dir)
        ignores.extend([".svn", ".hg", ".git"])

        def callback(res):
            dependencies.extend(res)

        def is_ignored(res, is_dir=False):
            if is_dir:
                res = res + "/"
            for i in ignores:
                if fnmatch.fnmatch(res, i) or res.startswith(i):
                    return True
            return False

        def find_ignored(reslist, is_dir=False):
            return [res for res in reslist if is_ignored(res, is_dir)]

        pool = ThreadPool(processes=Parser.concurrency)
        dependencies = []

        for root, dirs, files in scandir.walk(dir):
            for d in find_ignored(dirs, True):
                logging.debug("%s is blacklisted" % d)
                dirs.remove(d)
            for f in find_ignored(files):
                logging.debug("%s is blacklisted" % d)
                files.remove(f)
            for name in files:
                pool.apply_async(Parser.parse_file, args = (os.path.join(root, name),), callback = callback)

        pool.close()
        pool.join()
        return dependencies

