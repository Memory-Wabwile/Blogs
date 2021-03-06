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


class Blogs(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer,primary_key = True )
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    blog = db.Column(db.String(255))
    time = db.Column(db.DateTime,default = datetime.utcnow)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    comment = db.relationship('Comment' , backref='blogs' , lazy='dynamic')
    

    @classmethod
    def get_blogs(cls, category):
        blogs= Blogs.query.filter_by(category=category).all()
        return blogs

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.blog}'


class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.Text(),nullable = False)
    name = db.Column(db.Integer , db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'),nullable = False)

    @classmethod
    def get_comment(id):
        comment= Comment.query.filter_by(id=id).all()
        return comment

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    # def delete_comment(self):
    #     db.session.add(self)
    #     db.session.commit()

   

    def __repr__(self):
        return f'{self.comment}'


class Quotes:
    def __init__(self , author,quote):

        # self.id =id
        self.author = author
        self.quote = quote


class Subscriber(db.Model):
  __tablename__='subscribers'

  id=db.Column(db.Integer,primary_key=True)
  email = db.Column(db.String(255),unique=True,index=True)

  def save_subscriber(self):
    db.session.add(self)
    db.session.commit()

  def __repr__(self):
    return f'Subscriber {self.email}'
    