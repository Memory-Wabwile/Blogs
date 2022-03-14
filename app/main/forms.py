from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SubmitField,SelectField
from wtforms import validators
from wtforms.validators import DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
  title = StringField(' title:',validators=[DataRequired()]) 
  blogs = StringField(' post:',validators=[DataRequired()]) 
  username= StringField(' username:',validators=[DataRequired()])
  category = SelectField("Choose category:",choices=[('Interview','Interview'),('Promotions','Promotions'),('Products','Products'),('PickupLines','PickupLines'),('Sports','Sports'),('Entertainment','Entertainment')])

  submit = SubmitField('Submit')

class CommentForm(FlaskForm):
  comment = TextAreaField(' Comment:',validators=[DataRequired()])
  submit = SubmitField('Submit') 

class BlogForm(FlaskForm):
    title = StringField('Your Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Interview','Interview'),('Promotion','Promotion'),('PickupLines','PickupLines'),('Products','Products'),('Sports','Sports'),('Entertainment','Entertainment')],validators=[DataRequired()])
    blog = TextAreaField('Your Blog', validators=[DataRequired()])
    
    submit = SubmitField('Submit')