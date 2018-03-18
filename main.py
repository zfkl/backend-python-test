"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app
from alayatodo.models import users, todos, db


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
        user_1 = users(username='user1', password='user1')
        user_2 = users(username='user2', password='user2')

        todo_1 = todos(1, 'Vivamus tempus', 0)
        todo_2 = todos(1, 'lorem ac odio', 0)
        todo_3 = todos(1, 'Ut congue odio', 0)
        todo_4 = todos(1, 'Sodales finibus', 0)
        todo_5 = todos(1, 'Accumsan nunc vitae', 0)
        todo_6 = todos(2, 'Lorem ipsum', 0)
        todo_7 = todos(2, 'In lacinia est', 0)
        todo_8 = todos(2, 'Odio varius gravida', 1)

        db.session.add(user_1)
        db.session.add(user_2)

        db.session.add(todo_1)
        db.session.add(todo_2)
        db.session.add(todo_3)
        db.session.add(todo_4)
        db.session.add(todo_5)
        db.session.add(todo_6)
        db.session.add(todo_7)
        db.session.add(todo_8)

        db.session.commit()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
