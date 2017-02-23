# super-sprinter-3000-Kroki1412

The application uses flask as a webframework and peewee as an ORM.

# How it works?

1. clone this git repository (obviously)
1. edit the `connect_str.txt` and put your database name into it (delete the placeholder text)
1. go to the directory where this README.md is located what you are reading now
1. run this command:

`sudo pip3 install --editable .`

5. If it runs without error (means: no red text), run these:

`export FLASK_APP=dojo`

`export FLASK_DEBUG=true`

6. create the database with this command:

`flask initdb`

7. finally, start the application:

`flask run`

Ideally this should start the server, and now you can reach it from your browser on this address:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

For the more lazy people run the following commands instead
`chmod u+x run.sh`
`sudo ./run.sh`

