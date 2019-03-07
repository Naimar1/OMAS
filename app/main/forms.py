from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import Required, Email, EqualTo, ValidationError
from wtforms.validators import Required
from ..models import Subscription

class ProductForm(FlaskForm):

    title = StringField('Post title',validators=[Required()])
    text = TextAreaField('text',validators=[Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField('Email address', validators=[Required(), Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self, email):
        email = Subscription.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already subscribed to our emailing list.')