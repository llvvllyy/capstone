# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, FileField
# from wtforms.validators import DataRequired, Length, FileAllowed

# class AddPestForm(FlaskForm):
#     pest_name = StringField('Pest Name', validators=[DataRequired(), Length(min=2, max=100)])
#     pest_damage = TextAreaField('Pest Damage', validators=[DataRequired()])
#     pest_cycle = TextAreaField('Pest Life Cycle', validators=[DataRequired()])
#     pest_control = TextAreaField('Pest Control', validators=[DataRequired()])
#     pest_photo = FileField('Add Pest Photo', validators=[FileAllowed(photos, 'Images only!')])
