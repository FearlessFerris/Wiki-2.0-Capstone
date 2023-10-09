from flask import Flask, request, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests, datetime

from models import db, connect_db, User, Search, Favorite
from forms import CreateUserForm, LoginUserForm, SearchPagesForm, EditUserFrom, AddFavoritePage

from api import SEARCH_PAGE_BASE, GET_PAGE_BASE



app = Flask(__name__)
t = datetime.datetime.today()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wikipedia'
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True 
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SECRET_KEY'] = 'imasecretkeyshh'
app.debug = True
toolbar = DebugToolbarExtension( app )
app.app_context().push()
connect_db(app)





@app.route('/')
def homepage():
    """ Routes to Application Homepage """

    form = SearchPagesForm()

    return render_template('homepage.html', form = form )

# Create User / Login / Profile -------------------------------------------------

@app.route('/create-user', methods = ['GET', 'POST'])
def create_user_form():
    """ Routes to display form and handle form submission """

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        dob = form.dob.data
        picture = form.picture.data
        User.create( username, password, email, dob, picture )
        
        return redirect('/')
    
    else:
        return render_template('create-user-form.html', form = form)



@app.route('/login', methods = ['GET', 'POST'])
def user_login():
    """ Routes to login User """

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login(username, password)

        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Incorrect Name or Password']
        
    return render_template('login.html', form = form )



@app.route('/logout')
def logout_user():
    """ Routes to logout user """

    session.pop('user_id')
    return redirect('/')



@app.route('/user-profile')
def show_profile():
    """ Routes to user profile page """

    user = User.query.get(session['user_id'])

    return render_template('user-profile.html', user = user )



@app.route('/edit-profile', methods = ['GET', 'POST'])
def edit_profile():
    """ Routes to edit profile information """

    form = EditUserFrom()
    user_id = session.get('user_id')

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        dob = form.dob.data
        picture = form.picture.data
        user = User.query.get_or_404( user_id )
        user.update_profile( username, email, dob, picture )
        flash(f'You have successfully updated your profile!')
        db.session.commit()
        
        return redirect('/')
    
    else:
        return render_template('edit-user.html', form = form )



# Search Pages -----------------------------------------------------------------

@app.route('/search-pages', methods = ['GET', 'POST'])
def search_pages():
    """ Routes to search pages based on form input """

    form = SearchPagesForm()
    
    if form.validate_on_submit():
        search_term = form.search_term.data
        url = SEARCH_PAGE_BASE
        response = requests.get( url, params = { 'q' : search_term })
        data = response.json()
        pages = data['pages']
        
        search_timestamp = t
        user_id = session.get('user_id')
        search = Search( search_term, search_timestamp, user_id )
        search.add_search_to_history()
        return render_template('search-pages.html', form = form, data = data, pages = pages )

    else:
        return redirect('/search-pages')
    


@app.route('/get-page')
def show_page_info():
    """ Routes to display selected page information """

    form = AddFavoritePage()

    page = request.args.get('title')
    url = f'{GET_PAGE_BASE}{page}'
    response = requests.get( url )
    data = response.json()
    favorited_page = data['title']
    
    html_url = f'{GET_PAGE_BASE}{page}/html'
    html_response = requests.get( html_url )
    html = html_response.text
    
    return render_template('page.html', data = data, html = html, favorited_page = favorited_page, form = form )



@app.route('/search-history')
def show_history():
    """ Routes to show users search history """ 

    if session.get('user_id'):
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = session['user_id'])
    
    else:
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = None)
    
    return render_template('search-history.html', searches = searches )



@app.route('/edit-searches', methods = ['GET', 'POST'])
def edit_search_history():
    """ Routes to edit user search history """

    if session.get('user_id'):
        user = User.query.get_or_404( session['user_id'] )
        searches = Search.query.order_by(Search.id.desc()).filter_by( user_id = user.id ).all()

        return render_template( 'edit-searches.html', searches = searches )
    
    else:
        return redirect( '/login' )



@app.route('/remove-history-item', methods = ['GET', 'POST'])
def remove_search_history_item():
    """ Routes to remove a user specified search history item """

    user = User.query.get_or_404( session['user_id'] )
    term = request.args.get( 'search_term' )
    timestamp = request.args.get( 'search_timestamp' )
    search = Search.query.filter_by( search_term = term, search_timestamp = timestamp, user_id = user.id ).first()
    print( search )
    Search.delete_search_item( search )

    return redirect( '/edit-searches' )



@app.route('/clear-history', methods = ['GET', 'POST'])
def clear_user_search_history():
    """ Routes to clear users search history """

    if session.get('user_id'):
        user = User.query.get_or_404( session['user_id'] )
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = session['user_id'])
        Search.clear_search_history( searches )

        return redirect( '/search-history' )
    
    else:
        return redirect( '/login' )



# Favorites -------------------------------------------------------------------------------

@app.route('/favorites', methods = ['GET', 'POST'])
def add_show_favorites():
    """ Routes to add and show users favorited pages """

    if session.get( 'user_id' ):
        user = User.query.get_or_404( session['user_id'] )
        favorites = Favorite.query.filter_by( user_id = user.id ).all()
        form = AddFavoritePage()
        back = request.referrer

        if form.validate_on_submit():
            favorited_page = request.args.get('favorited_page')
            favorited_timestamp = t
            user_id = user.id
            Favorite.add_to_favorites( favorited_page, favorited_timestamp, user_id )
        
            return redirect( back )
        
        else:
            favorites = Favorite.query.order_by(Favorite.id.desc()).filter_by( user_id = user.id ).all()
            return render_template('favorites.html', user = user, favorites = favorites, form = form )

    else:
        return redirect( '/login' )



@app.route('/edit-favorites', methods = ['GET', 'POST'])
def edit_user_favorites():
    """ Routes to edit user favorites """

    user = User.query.get_or_404( session['user_id'] )
    favorites = Favorite.query.order_by(Favorite.id.desc()).filter_by( user_id = user.id ).all()

    return render_template( 'edit-favorites.html', favorites = favorites )



@app.route('/remove-favorited-item', methods = ['GET', 'POST'])
def remove_favorited_item():
    """ Removes a favorited item from users favorites """

    user = User.query.get_or_404( session['user_id'] )
    page = request.args.get( 'favorited_page' )
    timestamp = request.args.get( 'favorited_timestamp' )
    favorite = Favorite.query.filter_by( favorited_page = page, favorited_timestamp = timestamp, user_id = user.id ).first()
    print( favorite )
    Favorite.delete_favorite( favorite )

    return redirect( '/edit-favorites' )



@app.route('/clear-favorites', methods = ['GET', 'POST'])
def clear_all_favorites():
    """ Routes to clear all user favorited pages """

    user = User.query.get_or_404( session['user_id'] )
    favorites = Favorite.query.filter_by( user_id = user.id ).all()

    
    Favorite.clear_all_favorites( favorites )

    return redirect( '/favorites' )


    
    





