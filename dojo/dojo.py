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
    DATABASE=os.path.join(app.root_path, 'flask_dojo.db'),
    SECRET_KEY='development key',
    USERNAME='kroki',
    PASSWORD='test123'
))
app.config.from_envvar('DOJO_SETTINGS', silent=True)


# This initialises the database by connecting to it and than creating the table.
def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Entries], safe=True)
    entry = Entries.create(get_counter=0,
                           post_counter=0)
    entry.save()


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
def show_app():
    return render_template('general.html')


@app.route('/request_counter', methods=['GET', 'POST'])
def request_counter():
    if request.method == 'POST':
        entry = Entries.get()
        entry.post_counter += 1
        entry.save()
    else:
        entry = Entries.get()
        entry.get_counter += 1
        entry.save()
    return redirect(url_for('show_app'))


@app.route('/statistics')
def statistics():
    flash('Here are the stats!')
    entrys = Entries.select()
    if entrys.where(Entries.get_counter != None or Entries.post_counter != None).exists():
        # I have no clue why this is needed but else the data is not avaliable.
        entry2 = Entries.get()
        return render_template('stats.html', Data=True, entry=entry2)
    else:
        return render_template('stats.html', Data=False)

# return redirect(url_for('show_app'))


# if __name__ == "__main__":
#    app.run()
