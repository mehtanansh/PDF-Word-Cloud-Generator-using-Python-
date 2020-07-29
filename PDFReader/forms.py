from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField,FileAllowed,FileRequired

class InputForm(FlaskForm):
	PDF = FileField('Drop PDF File here',validators=[FileAllowed(['pdf']),FileRequired()])
	Submit = SubmitField('Upload')