import os
import sys
import subprocess
import pandas as pd

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
# from sqlalchemy import MetaData

from utils.database import db  # Import db from your models.py
from utils import models


def run_shell_command(command, venv):
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=venv)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr.decode()}")
        sys.exit(1)


def create_and_migrate_db():
    os.environ['FLASK_APP'] = 'wiserank'

    # Initialize Flask App and SQLAlchemy
    app = Flask(__name__)

    # Configure SQLite database for development
    basedir = os.path.abspath('')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'wiserank.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Create All Tables
    with app.app_context():
        db.create_all()

    # Initialize Flask-Migrate
    Migrate(app, db)

    venv = os.environ.copy()

    run_shell_command("flask db init", venv)

    run_shell_command("flask db migrate -m 'Initial migration'", venv)

    run_shell_command("flask db upgrade", venv)


def load_items():
    basedir = os.path.abspath('')
    db_url = 'sqlite:///' + os.path.join(basedir, 'wiserank.db') # replace with other db if necessary

    engine = create_engine(db_url)
    session = Session(engine)

    data_path = "../data/parsed/"
    for filename in os.listdir(data_path):
        df = pd.read_csv(data_path+filename)
        for row in df.to_dict(orient='records'):
            session.add(models.Item(track=row["track"],
                                    link_id=row["link_id"],
                                    name=row["name"],
                                    meta=row["meta"]
                                    ))
    session.commit()

if __name__ == "__main__":
    create_and_migrate_db()
    load_items()
    print("Database created and migrated. Items loaded.")