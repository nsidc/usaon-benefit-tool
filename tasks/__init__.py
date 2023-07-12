from invoke import Collection

from . import db, env, test

ns = Collection()
ns.add_collection(db)
ns.add_collection(env)
ns.add_collection(test)
