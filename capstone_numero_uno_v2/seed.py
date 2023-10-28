""" Seed file / Sample Data for Wiki 2.0 Application """

from models import User, Search, Favorite, db, connect_db


db.drop_all()
db.create_all()
db.session.commit()



u1 = User.create( username = 'Stan Smith', password = 'stantheman', email = 'stanthemansmith@gmail.com', dob = '10-11-1989', picture = '' )
u2 = User.create( username = 'Stellio Kontos', password = 'stelliotheman', email = 'stelliotheman@gmail.com', dob = '07-16-1990', picture = '' )



s1 = Search( search_term = 'Python', search_timestamp = '2023-10-08T17:11:52+00:00', user_id = '1' )
s2 = Search( search_term = 'Aston Martin', search_timestamp = '2023-10-08T17:12:31+00:00', user_id = '2')



f1 = Favorite( favorited_page = 'Python', favorited_timestamp = '2023-10-08T17:14:56+00:00', user_id = '1' )
f2 = Favorite( favorited_page = 'Aston Martin', favorited_timestamp = '2023-10-08T17:15:32+00:00', user_id = '2' )

db.session.add( u1 )
db.session.add( u2 )
db.session.add( s1 )
db.session.add( s2 )
db.session.add( f1 )
db.session.add( f2 )
db.session.commit()









