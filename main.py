"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
import subprocess
import os

from docopt import docopt
from alayatodo import app
from alayatodo.models import Users, Todos, db

def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        # _run_sql('resources/database.sql')
        # _run_sql('resources/fixtures.sql')
        USER1 = Users(username='user1', password='user1')
        USER2 = Users(username='user2', password='user2')

        TODO1 = Todos(1, 'Vivamus tempus', 0)
        TODO2 = Todos(1, 'lorem ac odio', 0)
        TODO3 = Todos(1, 'Ut congue odio', 0)
        TODO4 = Todos(1, 'Sodales finibus', 0)
        TODO5 = Todos(1, 'Accumsan nunc vitae', 0)
        TODO6 = Todos(2, 'Lorem ipsum', 0)
        TODO7 = Todos(2, 'In lacinia est', 0)
        TODO8 = Todos(2, 'Odio varius gravida', 1)

        db.session.add(USER1)
        db.session.add(USER2)

        db.session.add(TODO1)
        db.session.add(TODO2)
        db.session.add(TODO3)
        db.session.add(TODO4)
        db.session.add(TODO5)
        db.session.add(TODO6)
        db.session.add(TODO7)
        db.session.add(TODO8)

        db.session.commit()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
