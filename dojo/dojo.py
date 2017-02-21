# The extensive comments are for myself as I am new to flask and it helps with code purpose.
# all the imports
import os
from peewee import *
from dojo.connectdatabase import ConnectDatabase
from dojo.models import Entries
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app


app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , susp.py
app.debug = True  # This is for having debbuging turned on and not have to run it manualy.


# Load default config and override config from an environment variable
# The SECRET_KEY is needed to keep the client-side sessions secure. Choose
# that key wisely and as hard to guess and complex as possible.
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'susp.db'),
    SECRET_KEY='development key',
    USERNAME='kroki',
    PASSWORD='test123'
))
app.config.from_envvar('SUSP_SETTINGS', silent=True)


# This initialises the database by connecting to it and than creating the table.
def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Entries], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


#---------------------------------------

# base webpage
@app.route('/')
def show_entries():
    entries = Entries.select().order_by(Entries.id.desc())
    return render_template('list.html', entries=entries)


# this lists the entries. it basicly redirects to the root. XD
@app.route('/list')
def show_list():
    return show_entries()


# Editor page
@app.route('/story/<int:user_id>')
def show_story(user_id):
    entry = Entries.select().where(Entries.id == user_id)
    if entry.where(Entries.id == user_id).exists():
        # I have no clue why this is needed but else the data is not avaliable.
        entry2 = Entries.get(Entries.id == user_id)
        return render_template('form.html', new=False, entry=entry2)
    else:
        return show_entries()


# create new story
@app.route('/story')
def show_editor():
    return render_template('form.html', new=True)


# add this part will add a user story
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    if business_value(request.form['businessvalue']) is False:
        flash('Busniss value must be between 100 an 1500 and devidable by 100.')
        return show_editor()
    if estimation_value(request.form['estimation']) is False:
        flash('The estimation must be between 0.5 and 40 and devidable by 0.5.')
        return show_editor()
    new_entry = Entries.create(story_title=request.form['storytitle'],
                               user_story=request.form['userstory'],
                               accepting_criteria=request.form['acceptingcriteria'],
                               business_value=request.form['businessvalue'],
                               estimation=request.form['estimation'],
                               status=request.form['status'])
    new_entry.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


# this updates an entry
@app.route('/update/<int:user_id>', methods=['POST'])
def update_entry(user_id):
    if not session.get('logged_in'):
        abort(401)
    if business_value(request.form['businessvalue']) is False:
        flash('Busniss value must be between 100 an 1500 and devidable by 100.')
        return show_editor()
    if estimation_value(request.form['estimation']) is False:
        flash('The estimation must be between 0.5 and 40 and devidable by 0.5.')
        return show_editor()
    update_entry = Entries.update(story_title=request.form['storytitle'],
                                  user_story=request.form['userstory'],
                                  accepting_criteria=request.form['acceptingcriteria'],
                                  business_value=request.form['businessvalue'],
                                  estimation=request.form['estimation'],
                                  status=request.form['status']).where(Entries.id == user_id)
    update_entry.execute()
    flash('Entry was successfully edited')
    return show_entries()


# Delete entry
@app.route('/delete/<int:user_id>')
def delete_entry(user_id):
    entry = Entries.get(Entries.id == user_id)
    entry.delete_instance()
    return show_entries()


# this part will log in the user
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


# this part hadels the logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


def business_value(bvalue):
    bvalue = int(bvalue)
    if bvalue < 100:
        return False
    if bvalue > 1500:
        return False
    if bvalue % 100 == 0:
        return True
    else:
        return False


def estimation_value(evalue):
    evalue = float(evalue)
    if evalue < 0.5:
        return False
    if evalue > 40:
        return False
    if evalue % 0.5 == 0:
        return True
    else:
        return False

# if __name__ == "__main__":
#    app.run()
