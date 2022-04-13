import pymongo
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        try:
            g.db = pymongo.MongoClient(
                host='localhost',
                port=27017
            )
        except:
            click.echo("Error - Cannot connect to database")
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
