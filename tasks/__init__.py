from invoke import Collection

from . import db, test

ns = Collection()
ns.add_collection(db)
ns.add_collection(test)
