from datetime import datetime
from app import db , login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),index=True)
    email = db.Column(db.String(255),unique=True,index=True,nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    # pitchee = db.Column(db.Integer , db.ForeignKey('pitch.id'))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'User{self.username}'


class Pitches(db.Model):
    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True )
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    pitch = db.Column(db.String(255))
    time = db.Column(db.DateTime,default = datetime.utcnow)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    comment = db.relationship('Comment' , backref='pitches' , lazy='dynamic')
    upvote = db.relationship('Upvote' ,backref='pitches', lazy='dynamic' )
    downvote = db.relationship('Downvote' , backref='pitches' , lazy='dynamic')


    @classmethod
    def get_pitches(cls, category):
        pitches= Pitches.query.filter_by(category=category).all()
        return pitches

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def delete_pitch(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.pitch}'


class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.Text(),nullable = False)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'),nullable = False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.comment}'


class Upvote(db.Model):
    __tablename__='upvotes'

    id = db.Column(db.Integer,primary_key = True)
    upvote = db.Column(db.Integer)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))

    def save_upvote(self):
        db.session.add(self)
        db.session.commit()

    def delete_upvote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    def __repr__(self):
         return f'{self.user_id}:{self.post_id}'


class Downvote(db.Model):
    __tablename__='downvotes'

    id = db.Column(db.Integer,primary_key = True)
    downvote = db.Column(db.Integer)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))

    def save_downvote(self):
        db.session.add(self)
        db.session.commit()

    def delete_downvote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'downvote : {self.downvote}'
