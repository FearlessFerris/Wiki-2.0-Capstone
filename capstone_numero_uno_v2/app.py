from flask import Flask, request, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests, datetime

from models import db, connect_db, User, Search, Favorite, Like
from forms import CreateUserForm, LoginUserForm, SearchPagesForm, EditUserFrom, AddFavoritePage, LikePage

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
        flash( f'You have successfully created { username }' )
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



# Search Pages --------------------------------------------------------------------->

@app.route('/search-pages', methods = ['GET', 'POST'])
def search_pages():
    """ Routes to search pages based on form input """

    form = SearchPagesForm()
    
    if form.validate_on_submit():
        search_term = form.search_term.data
        url = SEARCH_PAGE_BASE
        response = requests.get( url, params = { 'q' : search_term, 'limit': 100 })
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
    form = LikePage()

    page = request.args.get('title')
    url = f'{GET_PAGE_BASE}{page}'
    response = requests.get( url )
    data = response.json()
    favorited_page = data['title']
    liked_page = data['title']

    html_url = f'{GET_PAGE_BASE}{page}/html'
    html_response = requests.get( html_url )
    html = html_response.text
    
    
    return render_template('page.html', data = data, html = html, favorited_page = favorited_page, liked_page = liked_page, form = form )



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
    Search.delete_search_item( search )
    flash( f'You have successfully removed { term } from your search history!' )

    return redirect( '/edit-searches' )



@app.route('/clear-history', methods = ['GET', 'POST'])
def clear_user_search_history():
    """ Routes to clear users search history """

    if session.get('user_id'):
        user = User.query.get_or_404( session['user_id'] )
        searches = Search.query.order_by(Search.id.desc()).filter_by(user_id = session['user_id'])
        Search.clear_search_history( searches )
        flash( f'You have successfully cleared your search history!' )

        return redirect( '/search-history' )
    
    else:
        return redirect( '/login' )



# Favorites ------------------------------------------------------------------------------->

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
            if favorited_page not in [ i.favorited_page for i in favorites ]:
                flash( f'You have successfully added { favorited_page } to your favorited pages!' )
                return redirect( back )
            else:
                flash( f'You already have { favorited_page } in your favorites library, dont worry its safe!' )
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
    flash( f'You have successfully removed { page } from your library of favorited pages' )

    return redirect( '/edit-favorites' )



@app.route('/clear-favorites', methods = ['GET', 'POST'])
def clear_all_favorites():
    """ Routes to clear all user favorited pages """

    user = User.query.get_or_404( session['user_id'] )
    favorites = Favorite.query.filter_by( user_id = user.id ).all()
    Favorite.clear_all_favorites( favorites )
    flash( f'You have successfully cleared all of your favorited items!' )

    return redirect( '/favorites' )


# Likes ---------------------------------------------------------------------------------->

@app.route( '/like-page', methods = ['GET', 'POST'])
def like_page():
    """ Routes to add a liked page to a users account """

    if session.get( 'user_id' ):
        user = User.query.get_or_404( session['user_id'] )
        likes = Like.query.order_by(Like.id.desc()).filter_by( user_id = user.id ).all()
        form = LikePage()
        back = request.referrer

        if form.validate_on_submit():
            liked_page = request.args.get( 'liked_page' )
            liked_timestamp = t
            user_id = user.id
            Like.add_to_likes( liked_page, liked_timestamp, user_id  )
            if liked_page not in [ i.liked_page for i in likes ]:
                flash( f'You have successfully added { liked_page } to your liked pages!' )
            else:
                flash( f'You already have { liked_page } in your liked pages library, dont worry its safe!' )
            return redirect( back )
        
        else:
            likes = Like.query.filter_by( user_id = user.id ).all()
            return render_template( 'liked-pages.html', likes = likes, form = form, user = user )

    else:
        return redirect( '/login' )



@app.route( '/edit-likes', methods = ['GET', 'POST'])
def edit_user_likes():
    """ Routes to edit a users liked pages """

    user = User.query.get_or_404( session['user_id'] )
    likes = Like.query.filter_by( user_id = user.id ).all()

    return render_template( 'edit-likes.html', user = user, likes = likes )



@app.route( '/remove-liked-item', methods = ['GET', 'POST'])
def remove_liked_item():
    """ Routes to remove a user selected liked item """

    user = User.query.get_or_404( session['user_id'] )
    page = request.args.get( 'liked_page' )
    timestamp = request.args.get( 'liked_timestamp' )
    like = Like.query.filter_by( liked_page = page, liked_timestamp = timestamp, user_id = user.id ).first()
    Like.remove_liked_item( like )
    flash( f'You have successfully removed { page } from your library of liked pages!' )

    return redirect( '/edit-likes' )



@app.route( '/clear-likes', methods = ['GET', 'POST'])
def clear_likes():
    """ Routes to clear all users liked pages """

    user = User.query.get_or_404( session['user_id'])
    Likes = Like.query.order_by( Like.id.desc()).filter_by( user_id = user.id ).all()
    Like.clear_likes( Likes )
    flash( f'You have successfully cleared all of your liked pages!')
     
    return redirect( 'like-page' )
