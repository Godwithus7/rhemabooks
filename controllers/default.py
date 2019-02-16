# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

POSTS_PER_PAGE = 36
OPOSTS_PER_PAGE = 30

def gen_Layout():
    return dict()

def index():
    page = request.args(1,cast=int,default=0)
    start = page*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    books = db().select(db.books.ALL, orderby=db.books.category,limitby =(start,stop))
    return locals()

def download():
    return response.download(request, db)

@auth.requires_login()
def show():
    id = request.args(0, cast=int)
    book = db.books(id) or redirect(URL('index'))
    comment = db(db.commt.books==book.id).select(orderby=db.commt.created_on,limitby=(0,1)).first()
    db.commt.books.default = book.id
    db.commt.parent_commt.default = comment
    form = SQLFORM(db.commt).process()
    comments = db(db.commt.books==book.id).select(orderby=db.commt.created_on)
    page = request.args(1,cast=int,default=0)
    start = page*OPOSTS_PER_PAGE
    stop = start+OPOSTS_PER_PAGE
    other_books = db(db.books.author==book.author).select(db.books.ALL,limitby =(start,stop))
    related_books = db(db.books.category==book.category).select(db.books.ALL,limitby =(start,stop))
    return locals()

@auth.requires_membership('manager')
def manage():
    navCategories = db().select(db.category.ALL)
    navAuthor = db().select(db.authors.ALL)
    grid = SQLFORM.smartgrid(db.books,linked_tables=['category'])
    return dict(grid=grid)


def book_category():
    category_id = request.args(0,cast=int,default=0)
    category = db.category(category_id)
    start = category_id*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    books = db(db.books.category==category_id).select()
    return locals()

def book_author():
    author_id = request.args(0,cast=int,default=0)
    author = db.authors(author_id)
    start = author_id*POSTS_PER_PAGE
    stop = start+POSTS_PER_PAGE
    books = db(db.books.author==author_id).select()
    return locals()

def search_results():
    keyword = request.vars.keyword
    title_query = db.books.title.contains(keyword)
    # category_query = db.books.category.name.contains(keyword)
    # author_query = db.books.authors.name.contains(keyword)
    # books = db(title_query or category_query or author_query).select(orderby=db.books.title)
    books = db(title_query).select(orderby=db.books.title)
    return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
