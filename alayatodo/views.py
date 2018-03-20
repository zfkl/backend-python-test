from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash
    )
from collections import OrderedDict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    """
    Read a todo only with id, user_id, description if exist
    empty if not exist
    :param id: todo id
    :return: /todo (item)
    TODO: 404 if no todo
    TODO: Only can read own user todo
    """
    cur = g.db.execute("SELECT * FROM todos WHERE id =%s" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    """Authenticate users
    :param empty
    :return
    -Redirect user to Read todos and if user was logged in but tried to
    fill an empty string for create a new Todo, there will be an error_empty tag
    in template to update the Add Todo description.
    -if log fails, redirect to log.
    TODO:
     -add max retry
     -add forget credentials
     -add bearer token authentication
     -only read own users todo unless admin user
    """
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    if session.get('empty_description'):
        error_empty = True
        session.pop('empty_description', None)
    return render_template('todos.html', **locals())


@app.route('/todo/', methods=['POST'])
def todos_POST():
    """This view is for Create todo:
    -Create a new Todo that is not empty string. There must be the 'description'
    tag in request form  or it will be a todo Update.
    There will be a flash message and change in placeholder to notify the end user
    if the string is empty.
    database updated and front end with new todo at bottom
    :param empty
    :return /todo (list of todos) or /login if not logged
    """
    req = request
    if not session.get('logged_in'):
        return redirect('/login')
    todo_description = request.form.get('description', '')
    if not todo_description:
        flash('Please add your todo description')
        session['empty_description'] = True
        return redirect('/todo')
    g.db.execute(
        "INSERT INTO todos (user_id, description, is_completed) VALUES (%s, '%s', %s)"
        % (session['user']['id'], todo_description, 0)
    )
    g.db.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    """
    Delete a todo from database, thus from front end
    :param id: todo id
    :return: redirect to login if not logged in
    redirect to /todo (list of todos)
    """
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id =%s" % id)
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/?is_completed=<is_completed>&id=<id>', methods=['POST'])
def todo_update(id, is_completed):
    """
    Update todo with its is_completed value 0/1, update checkbox checked/not checked
    :param id: todo id
    :param is_completed: with values 'True' or 'False' to be converted in 1 or 0 respectively
    :return: redirect to login if not logged in
    redirect to /todo (list of todos)
    """
    req = request
    if not session.get('logged_in'):
        return redirect('/login')
    is_completed = int(is_completed == 'True')
    cur = g.db.execute(
        "UPDATE todos SET is_completed = %s where id =%s AND user_id = %s" % (is_completed, id, session['user']['id'])
    )

    if cur.rowcount == 0:
        raise NotFound("It is not your task")
    g.db.commit()
    return redirect('/todo')
