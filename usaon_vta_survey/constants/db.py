import os

# Talk to a container called `db` at port 5432 by default:
DB_HOSTNAME = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', 5432)

DB_USERNAME = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

DB_CONNSTR = (
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}'
    f'@{DB_HOSTNAME}:{DB_PORT}/seaice'
)
