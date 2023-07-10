from invoke import Collection

from . import db, env, test
from . import format as format_

ns = Collection()
ns.add_collection(db)
ns.add_collection(env)
ns.add_collection(format_)
ns.add_collection(test)
