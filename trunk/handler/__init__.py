from os.path import dirname, basename, isdir, join
from glob import glob

filetypes = {}

# based on QuodLibet Code /formats/__init__
base = dirname(__file__)
self = basename(base)
modules = [f[:-3] for f in glob(join(base, "[!_]*.py"))]
modules = ["%s.%s" % (self, basename(m)) for m in modules]

for name in modules:
    handler = __import__(name, globals(), locals(), self)
    try:
        filetypes[handler.mime_type] = handler.keywords
    except:
        pass
# / Ende QuodLibet Code
       
del modules
del self
del base
