from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float, LargeBinary
from flask_login import UserMixin
from datetime import datetime
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename

db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(299), unique=True, nullable=False)
    firstname = db.Column(db.String(299), nullable=False)
    lastname = db.Column(db.String(299), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(299), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.user_id)

class UpdatePestForm(FlaskForm):
    pest_name = StringField('Pest Name', validators=[DataRequired(), Length(min=2, max=100)])
    pest_damage = TextAreaField('Pest Damage', validators=[DataRequired()])
    pest_cycle = TextAreaField('Pest Life Cycle', validators=[DataRequired()])
    pest_control = TextAreaField('Pest Control', validators=[DataRequired()])
    pest_photo = FileField('Update Pest Photo', validators=[FileAllowed(photos, 'Images only!')])

class Pest(db.Model):
    __tablename__ = 'pest'

    pest_id = db.Column(db.Integer, primary_key=True)
    pest_name = db.Column(db.String(299), unique=True, nullable=False)
    pest_damage = db.Column(db.Text, nullable=True)
    pest_cycle = db.Column(db.Text, nullable=True)
    pest_control = db.Column(db.Text, nullable=True)
    pest_photo = db.Column(db.String(255))

    def get_id(self):
        return str(self.pest_id)

class Corn(db.Model):
    __tablename__ = 'corn'

    corn_id = db.Column(db.Integer, primary_key=True)
    variety_name = db.Column(db.String(255), unique=True, nullable=False)
    year = db.Column(db.Integer)
    nsic_regnum = db.Column(db.String(200))
    variety_type = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    domain = db.Column(db.String(100))
    corn_yield = db.Column(db.Float)
    height_dry = db.Column(db.Float)
    height_wet = db.Column(db.Float)
    ear_length = db.Column(db.Float)
    shelling = db.Column(db.String(100))
    lodging = db.Column(db.String(100))
    reaction = db.Column(db.String(255))
    climate = db.Column(db.Text)
    image = db.Column(db.String(255))

    def __init__(self, variety_name, year, nsic_regnum, variety_type, owner, domain, corn_yield, 
                 height_dry, height_wet, ear_length, shelling, lodging, reaction, climate, image, **kwargs):
        self.variety_name = variety_name
        self.year = year
        self.nsic_regnum = nsic_regnum
        self.variety_type = variety_type
        self.owner = owner
        self.domain = domain
        self.corn_yield = corn_yield
        self.height_dry = height_dry
        self.height_wet = height_wet
        self.ear_length = ear_length
        self.shelling = shelling
        self.lodging = lodging
        self.reaction = reaction
        self.climate = climate
        # self.image = secure_filename(image).decode('utf-8') if image else None

    # def get_image_url(self):
        # return f'/static/images/corn_images/{self.image}'  # Adjust the path as needed


    def __repr__(self):
        return f'<Corn {self.variety_name}>'

class UserHistory(db.Model):
    __tablename__ = 'user_history'

    hist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hist_action = db.Column(db.String(255), nullable=False)
    hist_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    hist_details = db.Column(db.Text, default="")
    # Define a relationship with the User model
    user = db.relationship('User', backref=db.backref('history_entries', lazy=True))

    def __repr__(self):
        return f'<UserHistory {self.hist_id}>'