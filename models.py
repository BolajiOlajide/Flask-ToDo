"""
Define SQLAlchemy models.

The SQLAlchemy models for the database is defined here.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Set up the User model.

    Set up the properties of the User object and the table name too.
    """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True,
                         nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now(),
        onupdate=datetime.now(), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the User object.
        """
        return '<User: {}>'.format(self.username)


class Todo(db.Model):
    """
    Set up the BucketList model.

    Define the properties of the BucketList object and the table name too.
    """

    __tablename__ = 'Todo'
    __table_args__ = (db.UniqueConstraint(
        'name', 'created_by', name='unique_constraint_todo'),)
    todo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                           nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the BucketList object.
        """
        return '<Todo: {}>'.format(self.name)
