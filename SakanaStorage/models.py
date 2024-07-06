from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20), unique=True, nullable=False)
    filepath = db.Column(db.String(100), unique=True, nullable=False)
    # can add some meta information about the file here, for PATCH requests to modify, let's say
