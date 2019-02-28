from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    text = TextAreaField('text',validators=[Required()])
    category = SelectField('Type',choices=[('students','Students pitch'),('courses','Courses pitch')],validators=[Required()])
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    title = StringField('Comment title',validators=[Required()])
    comment = TextAreaField('Pitch Comment')
    submit = SubmitField('Submit')