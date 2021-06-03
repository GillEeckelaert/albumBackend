from sqlalchemy.orm import backref
from sqlalchemy.ext.associationproxy import association_proxy
from .. import db

UserSerie = db.Table('UserSerie',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('Users.id')),
    db.Column('serieId', db.Integer, db.ForeignKey('Series.id')),
    db.Column('read', db.Integer))

UserCollection = db.Table('UserCollection',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('Users.id')),
    db.Column('collectionId', db.Integer, db.ForeignKey('Collections.id')))

AuthorBook = db.Table('AuthorBook',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('authorId', db.Integer, db.ForeignKey('Authors.id')),
    db.Column('bookId', db.Integer, db.ForeignKey('Books.id')))

UserEvent = db.Table('UserEvent',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('Users.id')),
    db.Column('eventId', db.Integer, db.ForeignKey('Events.id')))

class UserBook(db.Model):
    __tablename__ = 'UserBooks'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('Users.id'))
    bookId = db.Column(db.Integer, db.ForeignKey('Books.id'))
    read = db.Column(db.Integer)
    #user = db.relationship("User", backref=backref("book_associations",cascade="all, delete-orphan"), lazy='subquery')
    #book = db.relationship("Book", backref=backref("user_associations",cascade="all, delete-orphan"), lazy='subquery')
    user = db.relationship("User", backref="UserBooks")
    book = db.relationship("Book", backref="UserBooks")

    def __init__(self, user=None, book=None, read=0):
        self.user = user
        self.book = book
        self.read = read

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column( db.DateTime, index=False, unique=False, nullable=False)
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    books = db.relationship("UserBook", backref="User")
    series = db.relationship("Serie", secondary=UserSerie , backref="Owner")
    collections = db.relationship("Collection", secondary=UserCollection , backref="Owner")
    events = db.relationship("Event", secondary=UserEvent, backref="User")
    #books = association_proxy('book_associations', 'book')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Serie(db.Model):
    __tablename__ = 'Series'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.id'))
    books = db.relationship('Book', backref='Serie' )

    def __repr__(self):
        return '<Serie {}>'.format(self.title)

class Collection(db.Model):
    __tablename__ = 'Collections'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    books = db.relationship('Book', backref='Collection')
    series = db.relationship('Serie', backref='Collection')

    def __repr__(self):
        return '<Serie {}>'.format(self.title)


class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    category = db.Column(db.String)
    price = db.Column(db.Float)
    purchaseDate = db.Column(db.DateTime)
    edition = db.Column(db.String)
    type = db.Column(db.String)
    language = db.Column(db.String)
    pages = db.Column(db.Integer)
    authors = db.relationship('Author', secondary=AuthorBook, backref='Book' )
    serie_id = db.Column(db.Integer, db.ForeignKey('Series.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.id'))
    owners = db.relationship('UserBook', backref='Book' )
    #owners = association_proxy('user_associations', 'user')

    def __repr__(self):
        return '<Book {}>'.format(self.title)    

class Author(db.Model):
    __tablename__ = 'Authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    books = db.relationship("Book", secondary=AuthorBook, backref="Author")

    def __repr__(self):
        return '<Author {}>'.format(self.name)  

class Event(db.Model):
    __tablename__='Events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    type = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    ticketsAmount = db.Column(db.Integer)
    eticket = db.Column(db.Boolean)
    confirmation = db.Column(db.Boolean)
    country = db.Column(db.String)
    city = db.Column(db.String)
    venue = db.Column(db.String)
    price = db.Column(db.Float)
    seats = db.Column(db.String)
    users = db.relationship("User", secondary=UserEvent, backref="Event")

    def __repr__(self):
        return '<Event {}>'.format(self.title)  