from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app, db = create_app()

manage = Manager(app)
Migrate(app, db)

manage.add_command('db', MigrateCommand)

from app.views import *

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000)
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()