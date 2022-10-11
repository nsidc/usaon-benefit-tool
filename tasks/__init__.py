from invoke import Collection

from . import db
from . import format as format_
from . import test

ns = Collection()
ns.add_collection(db)
ns.add_collection(format_)
ns.add_collection(test)
