from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Policy(FlaskForm):
    comment = TextAreaField("Política Pública", validators=[DataRequired()])
    submit = SubmitField('Proponer')
