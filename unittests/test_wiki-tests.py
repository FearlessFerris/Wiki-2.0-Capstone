from app import app
from flask_sqlalchemy import SQLAlchemy
from flask import session
from models import db, connect_db, User, Search, Favorite 
from unittest import TestCase


class WikiViewsTestCase( TestCase ):
    """ Homepage View Function Test Case """


    def test_homepage( self ):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'Homepage', html )



    def test_create_user( self ):
        with app.test_client() as client:
            res = client.get( '/create-user' )
            data = res.get_data( as_text = True )
            
            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'Create New User', data )
            


    def test_create_user_submit( self ):
        with app.test_client() as client:

            res = client.post('/create-user', data = { 'username': 'John', 'password': '123456', 'email': 'john46@gmail.com', 'dob': '1990-08-04', 'picture': '' } )
            data = res.get_data( as_text = True )
        
            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'value="John"', data )
            self.assertIn( 'value="john46@gmail.com"', data )



    def test_logout( self ):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 1

            res = client.get('/logout')
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 302 )
            self.assertEqual( res.location, '/' )
            self.assertIn( 'Redirecting', data )



    def test_login_user( self ):
        with app.test_client() as client:

            res = client.get( '/login' )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'Login </button>', data )
            


    def test_login_user_submit( self ):
        with app.test_client() as client:

            res = client.post( '/login', data = { 'username': 'John', 'password': '123456' })
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'value="John"', data )
    


    def test_edit_profile( self ):
        with app.test_client() as client:

            res = client.get( '/edit-profile' )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'Update </button>', data )
    

    def test_edit_profile_submit( self ):
        with app.test_client() as client:

            res = client.post( '/edit-profile', data = { 'username': 'Jimmy', 'email': 'jimmy20@gmail.com', 'dob': '1991-07-18', 'picture': '' })
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'value="Jimmy"', data )
            self.assertIn( 'value="jimmy20@gmail.com"', data )
    


    def test_search_pages( self ):
        with app.test_client () as client:

            res = client.get( '/search-pages' ) 
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 302 )
            self.assertIn( 'Redirecting', data )
    


    def test_search_pages_submit( self ):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 1

            res = client.post( '/search-pages', data = { 'search_term': 'Python' } )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( '(programming language)', data )
    


    def test_get_page( self ):
        with app.test_client() as client:

            res = client.get( '/get-page' )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( '/favorites?favorited_page', data )

    

    def test_search_history( self ):
        with app.test_client() as client:

            res = client.get( '/search-history' )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 ) 
            self.assertIn( '/clear-history', data )
    


    def test_clear_history_submit( self ):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                change_session['user_id'] = 1

            res = client.post( '/clear-history', follow_redirects = True )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( '<title>   Search History  </title>', data )
    


    def test_add_show_favorites( self ):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                change_session['user_id'] = 1 

            res = client.get( '/favorites' )
            data = res.get_data( as_text = True )

            self.assertEqual( res.status_code, 200 )
            self.assertIn( 'Edit Favorites', data )


    
    def test_add_show_favorites_submit( self ):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                change_session['user_id'] = 1 
        
        res = client.post( '/favorites', query_string = { 'favorited_page': 'food' }, data = { 'favorited_timestamp': '2023-10-02T01:17:38+00:00', 'user_id': '1' } )
        data = res.get_data( as_text = True )

        self.assertEqual( res.status_code, 302 )
        self.assertIn( 'Redirecting', data )



class UserModelTestCase( TestCase ):
    """ User Model Test Cases """



    def setUp( self ):
        """ This is ran before all tests """

        print( '*******************************************' )
        print( 'This setUp() method is ran before all tests' )



    def test_user_create( self ):
        """ Tests Creating a new User """

        username = 'SomeoneNew'
        password = '123456'
        email = 'someone@gmail.com'
        dob = '10-27-2023'
        picture = '' 

        someone = User.create( username = username, password = password, email = email, dob = dob, picture = picture )

        self.assertEqual( someone.username, 'SomeoneNew' )
        self.assertEqual( someone.email, 'someone@gmail.com' )



    def test_user_login( self ):

        username = 'SomeoneNew'
        password = '123456'

        someone = User.login( username = username, password = password )

        self.assertEqual( someone.password, someone.password )



class SearchModelTestCase( TestCase ):
    """ Search Model Test Cases """

    

    def test_add_search_to_history( self ):
        """ Test adding search to user history """

        s1 = Search( 'Someone', '2023-10-08T17:45:58+00:00', '1' )

        self.assertEqual(s1.add_search_to_history(), f'Someone || 2023-10-08T17:45:58+00:00 || 1' )



    def test_delete_search_item( self ):
        """ Test deleting a user search term """
        
        s1 = Search.query.filter_by( search_term = 'Aston Martin' ).first()
        print( s1 )

        Search.delete_search_item( s1 )

        self.assertNotEqual( s1, Search.query.filter_by( search_term = 'Aston Martin' ).first() )
    


    def test_clear_search_history( self ):
        """ Test clearing of a users search history """

        searches = Search.query.filter_by( user_id = 1 ).all()
        print( searches )

        Search.clear_search_history( searches )

        self.assertNotEqual( searches, Search.query.filter_by( user_id = 1 ).all() )



class FavoriteModelTestCase( TestCase ):
    """ Favorite Model Test Case """



    def test_add_to_favorites( self ):
        """ Test adding a page to users favorited page """

        fav = Favorite.add_to_favorites( 'McDonnell Douglas F-15 Eagle', '2023-10-08T23:37:22+00:00', '1' )

        self.assertEqual( fav.favorited_page, 'McDonnell Douglas F-15 Eagle' )
    


    def test_delete_favorite( self ):
        """ Test deleting a user favorited page """

        fav = Favorite.query.filter_by( favorited_page = 'McDonnell Douglas F-15 Eagle' ).first()

        self.assertNotIn( 'McDonnell Douglas F-15 Eagle', Favorite.query.filter_by( favorited_page = 'McDonnell Douglas F-15 Eagle' ).all() )


    
    def test_clear_all_favorites( self ):
        """ Test clearing all user favorited pages """


        favorites = Favorite.query.filter_by( user_id = '1' ).all()
        Favorite.clear_all_favorites( favorites )

        self.assertNotIn( 'McDonnell Douglas F-15 Eagle', Favorite.query.filter_by( favorited_page = 'McDonnell Douglas F-15 Eagle').all() )


        












        
        
        

        











                        
            











            


    




            
