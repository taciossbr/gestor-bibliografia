import sqlite3

import config

from . import dao
from . import models

def make_connection():
    return sqlite3.connect(config.DATABASE_URL)