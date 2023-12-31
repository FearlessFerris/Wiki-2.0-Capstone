from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# Create an Instance of SQLAlchemy & save to variable db

db = SQLAlchemy()
bcrypt = Bcrypt()
def connect_db(app):
    db.app = app
    db.init_app(app)






# User Model ------------------------------------------------------------------------------->

class User( db.Model ):
    """ User Model Instance """

    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    username = db.Column( db.Text, nullable = False, unique = True )
    password = db.Column( db.Text, nullable = False )
    email = db.Column( db.Text, nullable = False, unique = True )
    dob = db.Column( db.Date, nullable = False )
    picture = db.Column( db.Text, nullable = True )

    def __init__( self, username, password, email, dob, picture ):
        """ Initalize the attributes of the User Class """

        s = self
        s.username = username
        s.password = password
        s.email = email
        s.dob = dob
        s.picture = picture

    def __repr__(self):
        """ Representation Method of User Class """

        s = self 

        return f'User || id = { s.id } || username = { s.username } || password = { s.password } || email = { s.email } || dob = { s.dob } || picture_url = { s.picture } || searches = { s.searches }'
    
    def update_profile( self, username, email, dob, picture ):
        """ Update user profile information of a User Instance """

        s = self
        s.username = username
        s.dob = dob
        s.email = email
        s.picture = picture

        return f'You have successfully updated your profile: { s.username } || { s.email } || { s.dob } || { s.picture }'

    @classmethod
    def create( cls, username, password, email, dob, picture ):
        """ Creates a new user """

        hashed = bcrypt.generate_password_hash( password )
        hashed_utf8 = hashed.decode( 'utf-8' )
        password = hashed_utf8
        new_user = User( username, password, email, dob, picture )
        db.session.add( new_user )
        db.session.commit()

        return new_user
    
    @classmethod
    def login( cls, username, password ):
        """ Authenticate User and Authorize User Login """

        user = User.query.filter_by( username = username ).first()

        if user and bcrypt.check_password_hash( user.password, password ):
            return user
        else:
            return False


# Search Model ------------------------------------------------------------------------------> 

class Search( db.Model ):
    """ Search Model Instance """

    __tablename__ = 'searches'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    search_term = db.Column( db.Text, nullable = True )
    search_timestamp = db.Column( db.Text, nullable = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )

    users = db.relationship( 'User', backref = 'searches' )

    def __init__( self, search_term, search_timestamp, user_id ):
        """ Initalize the attributes of the Search class """

        s = self
        s.search_term = search_term
        s.search_timestamp = search_timestamp
        s.user_id = user_id
        
    def __repr__(self):
        """ Representation Method of Search Class """

        s = self

        return f'Search || search_term = { s.search_term } || search_timestamp = { s.search_timestamp } || user_id = { s.user_id }' 

    def add_search_to_history( self ):
        """ Adds search to user search history """

        s = self
        search = Search( s.search_term, s.search_timestamp, s.user_id )
        db.session.add( search )
        db.session.commit()
        return f'{ s.search_term } || { s.search_timestamp } || { s.user_id }'    

    @classmethod
    def delete_search_item( cls, search ):
        """ Removes a search item from user search history """

        db.session.delete( search )
        db.session.commit()
        return search
    
    @classmethod
    def clear_search_history( cls, searches ):
        """ Clears users search history """
        
        for search in searches:
            db.session.delete( search )
            db.session.commit()
        
        return searches
    


# Favorite Model ----------------------------------------------------------------------------->

class Favorite( db.Model ):
    """ Favorite Model Instance """

    __tablename__ = 'favorites'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    favorited_page = db.Column( db.Text, nullable = True )
    favorited_timestamp = db.Column( db.Text, nullable = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ))

    user = db.relationship( 'User', backref = 'favorites' )

    def __init__( self, favorited_page, favorited_timestamp, user_id ):
        """ Initalize the attributes of the Favorite class """

        s = self
        s.favorited_page = favorited_page
        s.favorited_timestamp = favorited_timestamp
        s.user_id = user_id

    def __repr__(self):
        """ Representation Method of Favorite """

        s = self

        return f'Favorite || favorited_page = { s.favorited_page } || favorited_timestamp = { s.favorited_timestamp } || user_id = { s.user_id }'
    
    @classmethod
    def add_to_favorites( cls, favorited_page, favorited_timestamp, user_id ):
        """ Add page to user favorited pages """
        
        Favorites = Favorite.query.filter_by( user_id = user_id ).all()
        new_fav = Favorite( favorited_page, favorited_timestamp, user_id )
        if new_fav.favorited_page not in [ i.favorited_page for i in Favorites ]:
            db.session.add( new_fav )
            db.session.commit()

        return new_fav
    
    @classmethod 
    def delete_favorite( cls, favorite ):
        """ Deletes a specific user favorited page """

        db.session.delete( favorite )
        db.session.commit()

        return favorite
    

    @classmethod 
    def clear_all_favorites( cls, favorites ):
        """ Routes to clear all user favorited pages """

        for fav in favorites:
            db.session.delete( fav )
            db.session.commit()
        
        return favorites
    
# Like Model ------------------------------------------------------------------------------->

class Like( db.Model ):
    """ Likes model Instance """

    __tablename__ = 'likes'

    id = db.Column( db.Integer, primary_key = True, autoincrement = True, unique = True )
    liked_page = db.Column( db.Text, nullable = True )
    liked_timestamp = db.Column( db.Text, nullable = True )
    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )

    user = db.relationship( 'User', backref = 'likes' )

    def __init__( self, liked_page, liked_timestamp, user_id ):
        """ Initalize the attributes of the Like class """

        s = self
        s.liked_page = liked_page
        s.liked_timestamp = liked_timestamp
        s.user_id = user_id

    def __repr__( self ):
        """ Representation method of Like class """

        s = self

        return f'Like || liked_page = { s.liked_page } || liked_timestamp = { s.liked_timestamp } || User_id = { s.user_id }'
    
    @classmethod
    def add_to_likes( cls, liked_page, liked_timestamp, user_id ):
        """ Add a page to a users liked pages """

        Likes = Like.query.filter_by( user_id = user_id ).all()
        new_like = Like( liked_page, liked_timestamp, user_id )
        if new_like.liked_page not in [ i.liked_page for i in Likes ]:
            db.session.add( new_like )
            db.session.commit()
        
        return new_like 
    
    @classmethod
    def remove_liked_item( cls, like ):
        """ Removes a user selected liked item """

        db.session.delete( like )
        db.session.commit()

        return like
    
    @classmethod 
    def clear_likes( cls, likes ):
        """ Clear all user likes """

        for i in likes:
            db.session.delete( i )
            db.session.commit()

        return likes






  


        

        
   

