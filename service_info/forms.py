from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ServiceInfoForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(), Length(min=2, max=120)])
    service_icon = StringField('Service Icon', validators=[DataRequired(), Length(min=10, max=20)])
    service_abstract = StringField('Service Abstract', validators=[DataRequired(), Length(min=2, max=240)])
    service_description = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField('Save')