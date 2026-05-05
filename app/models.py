# Marissa O'Meally
# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#Deshawn added UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    userID = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80)) 
    last_name = db.Column(db.String(80)) 
    email = db.Column(db.String(120), unique=True, nullable=False, index=True) 
    password = db.Column(db.String(128))
    
    date_of_birth =  db.Column(db.Date)
    
    gender = db.Column(db.String(15))
    looking_for = db.Column(db.String(20))
    
    bio = db.Column(db.Text)
    
    profile_visibility = db.Column(db.Boolean, default=True)
    
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    preferred_radius = db.Column(db.Integer)
    
    profile_picture = db.Column(db.String(120))
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    location = db.relationship('Location', backref='users')
    
    def __init__(self, username, first_name, last_name, email, password, date_of_birth, gender, looking_for, bio, locationID, preferred_radius, profile_picture, profile_visibility=True):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.looking_for = looking_for
        self.bio = bio
        self.profile_visibility = profile_visibility
        self.locationID = locationID
        self.preferred_radius = preferred_radius
        self.profile_picture = profile_picture
        
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    


    def get_id(self):
        return str(self.userID)
    def __repr__(self):
        return '<User %r>' % (self.username)
    
    
    

class Location(db.Model):
    __tablename__ = 'location'
    
    locationID = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    def __init__(self, city, country, latitude, longitude):
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
    
    
class Interest(db.Model):
    __tablename__ = 'interests'
    
    interestID = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String(120), unique=True)
    
    def __init__(self, interest_name):
        self.interest_name = interest_name 
 
    
class User_Interest(db.Model):
    __tablename__ = 'user_interests'
    
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True)
    interestID = db.Column(db.Integer, db.ForeignKey('interests.interestID'), primary_key=True)
    
    def __init__(self, userID, interestID):
        self.userID = userID
        self.interestID = interestID

    
class Match(db.Model):
    __tablename__ = 'matches'
    
    matchID = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.userID')) 
    user2_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    status = db.Column(db.String(25))
    mutual_match = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __init__(self, user1_id, user2_id, status, mutual_match):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.status = status
        self.mutual_match = mutual_match
        

class Message(db.Model):
    __tablename__ = 'messages'
    
    messageID = db.Column(db.Integer, primary_key=True)
    matchID = db.Column(db.Integer, db.ForeignKey('matches.matchID')) 
    senderID = db.Column(db.Integer, db.ForeignKey('users.userID')) 
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)
    
    def __init__(self, matchID, senderID, content):
        self.matchID = matchID
        self.senderID = senderID
        self.content = content
        
        
class Favourite(db.Model):
    __tablename__ = 'favourites'
    
    favouriteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    saved_user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __init__(self, userID, saved_user_id):
        self.userID = userID
        self.saved_user_id = saved_user_id
        
        
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notificationID = db.Column(db.Integer, primary_key=True)
    userID =  db.Column(db.Integer, db.ForeignKey('users.userID'))
    type = db.Column(db.String(50))
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __init__(self, userID, type, content):
        self.userID = userID
        self.type = type
        self.content = content
        
        