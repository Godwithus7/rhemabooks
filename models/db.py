# coding: utf8

db = DAL("sqlite://storage.sqlite")
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)

# import prettydate to concert datetime to min ago ot hours ago.
import datetime
d = datetime.datetime(2009,7,25,14,34,56)
from gluon.tools import prettydate
pretty_d = prettydate(d,T)

db.define_table('category', 
                Field('name','string',unique = True),
                format = '%(name)s')

db.define_table('authors', 
                Field('name','string', unique = True),
                Field('aboutauthor','text'),
                format = '%(name)s')

db.define_table('books',
                Field('category','reference category'),
                Field('author','reference authors'),
                Field('title','string'),
                Field('file', 'upload'),
                Field('aboutbook','text'),
                Field('price','float'),
                format = '%(title)s')

db.define_table('commt',
                Field('books', 'reference books'),
                Field('parent_commt','reference commt'),
                Field('comment', 'text'),
                auth.signature)

def author(id):
    if id is None:
        return "Unknown"
    else:
        user = db.auth_user(id)
        return '%(first_name)s %(last_name)s' % user

db.category.name.requires = (IS_NOT_IN_DB(db, db.category.name))
db.authors.name.requires = (IS_NOT_IN_DB(db, db.authors.name))
db.books.category.requires = (IS_IN_DB(db, db.category.id,'%(name)s'))
db.books.author.requires = (IS_IN_DB(db, db.authors.id,'%(name)s'))
db.authors.aboutauthor.requires = IS_NOT_EMPTY()
db.books.title.requires = IS_NOT_EMPTY()
db.books.file.requires = IS_NOT_EMPTY()
db.books.aboutbook.requires = IS_NOT_EMPTY()
db.books.price.requires = IS_NOT_EMPTY()
db.commt.comment.requires = IS_NOT_EMPTY()

db.books.category.writable = db.books.category.readable = True
db.books.author.writable = db.books.author.readable = True
db.commt.books.writable = db.commt.books.readable = False
db.commt.parent_commt.writable = db.commt.parent_commt.readable = False

navCategories = db().select(db.category.ALL)
navAuthor = db().select(db.authors.ALL)