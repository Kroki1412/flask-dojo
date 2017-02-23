sudo pip3 install --editable .
export FLASK_APP=dojo
export FLASK_DEBUG=true
flask initdb
flask run
