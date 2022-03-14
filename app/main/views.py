from flask import render_template,request,redirect,url_for,abort
from ..models import User
from ..models import User, Pitches,Comment,Upvote,Downvote
from . import main
from flask_login import current_user, login_required 
from .forms import UpdateProfile
from .. import db,photos
from .forms import PostForm,CommentForm,UpdateProfile,PitchForm
from flask.helpers import flash



@main.route('/')
def index():
    '''
    function that returns the index page and its data
    '''
    Interview=Pitches.query.filter_by(category='Interview').all()
    Promotion=Pitches.query.filter_by(category='Promotion').all()
    Products = Pitches.query.filter_by(category='Products').all()
    PickupLines = Pitches.query.filter_by(category='PickupLines').all
    Sports = Pitches.query.filter_by(category='Sports').all()
    Entertainment = Pitches.query.filter_by(category='Entertainment').all()
    pitch = Pitches.query.all()
    return render_template('index.html', Interview=Interview , Promotion=Promotion, Products=Products,PickupLines=PickupLines, Sports=Sports, Entertainment=Entertainment , pitch = pitch)



@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    pitch = Pitches.query.filter_by(name=user_id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user , pitch=pitch)


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


@main.route('/pitch',methods=['GET','POST'])
@login_required
def new_pitches():

    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        pitch = form.pitch.data
        id = current_user._get_current_object().id

        new_pitches = Pitches(title=title,pitch=pitch,category=category)
        db.session.add(new_pitches)
        db.session.commit()

        flash('successful')
        return redirect(url_for('main.index',form=form))

    return render_template('pitch.html', form=form)


@main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return('Sorry !! User not found try again')
    return render_template('profile.html',user=user)



@main.route('/comment/<int:pitch_id>', methods=['GET','POST'])
@login_required
def comment(pitch_id):

    form = CommentForm()

    
   

    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        name = current_user._get_current_object().id

        new_comment = Comment(comment=comment,pitch_id=pitch_id,name=name)

        new_comment.save_comment()
        flash('Comment added successfully')
        return redirect(url_for('.comment', pitch_id = pitch_id))
    
    pitch = Pitches.query.get(pitch_id)
    user = User.query.all()
    comments = Comment.query.all()

    return render_template('comment.html', form=form,comments=comments,pitch=pitch,user=user)
        


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Pitches.query.get(id)
    if post is None:
        abort(404)
        
    upvote= Upvote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if upvote is not None:
        
        db.session.delete(upvote)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    
    new_like = Upvote(
        user_id=current_user.id,
        pitch_id=id
        
    )
    db.session.add(new_like)
    db.session.commit()

        
    return redirect(url_for('main.index'))

@main.route('/dislike/<int:id>', methods=['POST', 'GET'])
@login_required
def downvote(id):
    post = Pitches.query.get(id)
    if post is None:
        abort(404)
        
    downvote= Downvote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if downvote is not None:
        
        db.session.delete(downvote)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    
    new_like = Downvote(
        user_id=current_user.id,
        pitch_id=id
        
    )
    # new_like.save()
    db.session.add(new_like)
    db.session.commit()

        
    return redirect(url_for('main.index'))