from flask import render_template,request,redirect,url_for,abort
from ..models import User
from ..models import User, Blogs,Comment,Upvote,Downvote
from . import main
from flask_login import current_user, login_required 
from .forms import UpdateProfile
from .. import db,photos
from .forms import PostForm,CommentForm,UpdateProfile,BlogForm
from flask.helpers import flash



@main.route('/')
def index():
    '''
    function that returns the index page and its data
    '''
    Interview=Blogs.query.filter_by(category='Interview').all()
    Promotion=Blogs.query.filter_by(category='Promotion').all()
    Products = Blogs.query.filter_by(category='Products').all()
    PickupLines = Blogs.query.filter_by(category='PickupLines').all
    Sports = Blogs.query.filter_by(category='Sports').all()
    Entertainment = Blogs.query.filter_by(category='Entertainment').all()
    blog = Blogs.query.all()
    return render_template('index.html', Interview=Interview , Promotion=Promotion, Products=Products,PickupLines=PickupLines, Sports=Sports, Entertainment=Entertainment , blog = blog)



@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    blog = Blogs.query.filter_by(name=user_id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user , blog=blog)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/blog',methods=['GET','POST'])
@login_required
def new_blogs():

    form = BlogForm()

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        blog = form.blog.data
        id = current_user._get_current_object().id

        new_blogs = Blogs(title=title,blog=blog,category=category)
        db.session.add(new_blogs)
        db.session.commit()

        flash('successful')
        return redirect(url_for('main.index',form=form))

    return render_template('blog.html', form=form)


@main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return('Sorry !! User not found try again')
    return render_template('profile.html',user=user)



@main.route('/comment/<int:blog_id>', methods=['GET','POST'])
@login_required
def comment(blog_id):

    form = CommentForm()

    
   

    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        name = current_user._get_current_object().id

        new_comment = Comment(comment=comment,blog_id=blog_id,name=name)

        new_comment.save_comment()
        flash('Comment added successfully')
        return redirect(url_for('.comment', blog_id = blog_id))
    
    blog = Blogs.query.get(blog_id)
    user = User.query.all()
    comments = Comment.query.all()

    return render_template('comment.html', form=form,comments=comments,blog=blog,user=user)
        


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Blogs.query.get(id)
    if post is None:
        abort(404)
        
    upvote= Upvote.query.filter_by(user_id=current_user.id, blog_id=id).first()
    if upvote is not None:
        
        db.session.delete(upvote)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    
    new_like = Upvote(
        user_id=current_user.id,
        blog_id=id
        
    )
    db.session.add(new_like)
    db.session.commit()

        
    return redirect(url_for('main.index'))

@main.route('/dislike/<int:id>', methods=['POST', 'GET'])
@login_required
def downvote(id):
    post = Blogs.query.get(id)
    if post is None:
        abort(404)
        
    downvote= Downvote.query.filter_by(user_id=current_user.id, blog_id=id).first()
    if downvote is not None:
        
        db.session.delete(downvote)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    
    new_like = Downvote(
        user_id=current_user.id,
        blog_id=id
        
    )
    # new_like.save()
    db.session.add(new_like)
    db.session.commit()

        
    return redirect(url_for('main.index'))