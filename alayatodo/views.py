"""
Execute logic part when user hits an endpoint with correct url route
todos/ for any listing of todos
todo/ for a single instance of Todo model

"""
import json

from alayatodo import app
from flask import (
    redirect,
    render_template,
    request,
    Response,
    session,
    flash
    )
from alayatodo.helpers import model_serializer, url_redirect
from alayatodo.models import Users, Todos, db
from werkzeug.exceptions import NotFound, Unauthorized


@app.route('/')
def home():
    """Give instruction for test"""
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login_get():
    """Render Login page functionnality"""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    """Process login for user
    serialize model to update session with 'user' tag
    update session with 'logged_in' tag
    redirect to login/ if no success
    """
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username).filter_by(password=password).first()
    if user:
        session['logged_in'] = True
        session['user'] = model_serializer(user)
        return redirect('/todos')

    return redirect('/login')


@app.route('/logout')
def logout():
    """update session with None for both 'logged_in' and 'user' tags
    redirect to home page
    """
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo_get(id):
    """
    Read a todo only with id, user_id, description if exist
    empty if not exist
    :param id: todo id
    :return: /todo (item)
    """

    todo_read = Todos.query.get(id)
    if todo_read is None:
        raise NotFound("todo not found")
    if todo_read.user_id != session['user']['id']:
        raise Unauthorized("Not your todo")
    return render_template('todo.html', todo=todo_read)


@app.route('/todos/', defaults={'page': 1}, methods=['GET'])
@app.route('/todos/?page=<page>', methods=['GET'])
def todos_get(page):
    """Authenticate users
    :param page to get data from the specific page
    :return
    -Redirect user to Read todos and if user was logged in but tried to
    fill an empty string for create a new Todo, there will be an error_empty tag
    in template to update the Add Todo description.
    -if log fails, redirect to log.
    Pagination for limit data read in UI, limit set with config param 'TODO_PER_PAGE'
    TODO:
     -add max retry
     -add forget credentials
     -add bearer token authentication
    """
    if not session.get('logged_in'):
        return redirect('/login')

    page = int(request.args.get('page', 1))

    # todos_read = todos.query.all()  # to keep for testing impersonification on UI
    todos_read = Todos.query.filter_by(user_id=session['user']['id']).paginate(
        page, app.config['TODO_PER_PAGE']).items
    if hasattr(session, 'empty_description'):
        error_empty = True
        setattr(session, 'empty_description', None)
    return render_template('todos.html', **locals())


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json_get(id):
    """
    Read json from todo data based on todo id
    :param id: todo id
    :return: json data for single todo
=    """
    if not session.get('logged_in'):
        return redirect('/login')

    todo_read = Todos.query.get(id)
    if todo_read is None:
        return NotFound("todo not found")

    if todo_read.user_id != session['user']['id']:
        raise Unauthorized("Not your todo")

    todo_dump = json.dumps(model_serializer(todo_read))
    return Response(todo_dump, status=200, mimetype='application/json')


@app.route('/todo/', methods=['POST'])
def todo_post():
    """This view is for Create todo:
    -Create a new Todo that is not empty string. There must be the 'description'
    tag in request form  or it will be a todo Update.
    There will be a flash message and change in placeholder to notify the end user
    if the string is empty.
    Flash message for Create todo confirmation
    database updated and front end with new todo at bottom.
    Add a todo and stay on the same page or go to the new page depending on pagination
    :param page of todo list
    :return /todo (list of todos) or /login if not logged
    """
    if not session.get('logged_in'):
        return redirect('/login')

    todo_description = request.form.get('description', '')
    if not todo_description:
        flash('Please add your todo description')
        session['empty_description'] = True
        url = url_redirect()
        return redirect(url)

    todo_inserted = Todos(user_id=session['user']['id'],
                          description=todo_description, is_completed=0)
    db.session.add(todo_inserted)
    db.session.commit()
    flash('Todo {} is added!'.format(todo_description))

    url = url_redirect(is_create=True)
    return redirect(url)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    """
    Delete a todo from database, thus from front end,
    flash message confirming deletion
    :param id: todo id
    :return: redirect to login if not logged in
    redirect to /todo (list of todos)
    """
    if not session.get('logged_in'):
        return redirect('/login')

    # cur = g.db.execute("SELECT description FROM todos WHERE id ='%s'" % id)
    # todo = cur.fetchone()
    todo_read = Todos.query.get(id)
    if todo_read is None:
        raise NotFound("todo to delete not found")

    todo_description = model_serializer(todo_read)['description']
    flash('Todo {} is removed!'.format(todo_description))
    todo_delete = Todos.query.get(id)
    db.session.delete(todo_delete)
    db.session.commit()

    url = url_redirect(is_delete=True)
    return redirect(url)


@app.route('/todo/?is_completed=<is_completed>&id=<id>', methods=['POST'])
def todo_update(id, is_completed):
    """
    Update todo with its is_completed value 0/1, update checkbox checked/not checked
    :param id: todo id
    :param is_completed: with values 'True' or 'False' to be converted in 1 or 0 respectively
    :param page of the list of todo
    :return: redirect to login if not logged in
    redirect to /todo/?page=page (list of todos), so the user stays on same page after update
    or goes to the new page depending on pagination
    """
    if not session.get('logged_in'):
        return redirect('/login')

    is_completed = int(is_completed == 'True')
    todo_updated = Todos.query.get(id)
    if todo_updated is None:
        raise NotFound("todo to update not found")

    if todo_updated.user_id != session['user']['id']:
        raise Unauthorized("Not your todo")

    todo_updated.is_completed = is_completed
    db.session.commit()

    url = url_redirect(is_update=True)
    return redirect(url)
