from datetime import datetime
import pandas as pd
from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, jsonify
)
from models import User, Corn, UserHistory, Pest, UpdatePestForm, photos, secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet, IMAGES
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from dt import C45DecisionTree
import base64

# app = Flask(__name__)
# app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/dss'
login_manager = LoginManager()  

# def create_app():
app = Flask(__name__)
app.config.from_object(Config)  # Replace with your actual config class

from models import db
app.config['UPLOADED_PHOTOS_DEST'] = 'static/corn_images'
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)   
    
    # return app

# from models import User, Corn, photos, UserHistory, Pest, UpdatePestForm, secure_filename
# app = create_app() 



def save_photo(photo_data):
    if photo_data:
        # Save the photo using Flask-Uploads
        filename = photos.save(photo_data)
        return filename
    # Return None if no photo is provided
    return None

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_photo():
#     form = UploadForm()

#     if form.validate_on_submit():
#         uploaded_photo = form.photo.data
#         filename = secure_filename(uploaded_photo.filename)
#         photos.save(uploaded_photo, name=filename)

#         # Additional processing or save filename to the database

#         return redirect(url_for('uploaded_photo', filename=filename))

#     return render_template('upload.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def initialize_admin():
    # Check if the admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Hash the password for the admin user
        hashed_password = generate_password_hash('admin1234', method='pbkdf2:sha1')

        # Create the admin user with the hashed password
        admin_user = User(username='admin', firstname='Admin', lastname='User', password=hashed_password, email='admin@example.com', is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created successfully.')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Authentication successful
            login_user(user)
            
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        
        else:
            # Authentication failed
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # Handle GET requests (display login page)
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user details from the registration form
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose a different username.', 'error')
            return redirect(url_for('register'))

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user instance
        new_user = User(username=username, firstname=firstname, lastname=lastname, password=hashed_password, email=email)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    # Handle GET requests (display registration form)
    return render_template('auth/register.html')

@app.route('/home')
@login_required
def home():
    user = current_user

    if user.is_admin:
        # Redirect to admin page
        return render_template('admin/admin.html', user=user)
    else:
        # Redirect to regular user dashboard
        return render_template('home.html', user=user)

@app.route('/aboutus')
@login_required
def aboutus():
    user = current_user
    return render_template('aboutus.html', user=user)

@app.route('/contact')
@login_required
def contact():
    user = current_user
    return render_template('contactus.html', user=user)

@app.route('/pest')
@login_required
def pest():
    user = current_user
    return render_template('pest.html', user=user)

@app.route('/admin')
@login_required
def admin():
    user = current_user
    if user.is_admin:
        # Render the admin template
        return render_template('admin/admin.html', user=user)
    else:
        # Redirect to home for non-admin users
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('home', user=user))

@app.route('/profile')
@login_required
def profile():
    user_history_entries = UserHistory.query.filter_by(user_id=current_user.user_id).all()
    return render_template('profile.html', user_history_entries=user_history_entries)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        # Handle the form submission, update user profile, etc.

        return render_template('edit_profile.html', user=user)
    
@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Handle the form submission, update user profile, etc.
        new_username = request.form.get('newUsername')
        new_firstname = request.form.get('newFirstname')
        new_lastname = request.form.get('newLastname')
        new_contact = request.form.get('newContact')

        # Update user profile
        current_user.username = new_username
        current_user.firstname = new_firstname
        current_user.lastname = new_lastname
        current_user.contact = new_contact

        # Commit changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')

    return redirect(url_for('profile'))

@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    if request.method == 'POST':
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')

        # Verify the old password
        if not check_password_hash(current_user.password, old_password):
            flash('Incorrect old password. Please try again.', 'error')
            return redirect(url_for('profile'))

        # Update the password
        current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()

        # Log out the user
        logout_user()

        flash('Password updated successfully. You have to login with your new password.', 'success')
        return redirect(url_for('login'))

    # Handle other HTTP methods if necessary
    return redirect(url_for('profile'))

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # Delete the user account
        db.session.delete(current_user)
        db.session.commit()

        # Log out the user
        logout_user()

        flash('Your account has been deleted. <br> We hate to see you go!', 'success')
        return redirect(url_for('login'))

    # Handle GET requests to display confirmation page
    return render_template('account_delete.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('Logout successful!', 'success')  # Add this line
    return redirect(url_for('login'))

@app.route('/show_user', methods=['POST'])
@login_required
def show_user():
    try:
        user_data = get_user_data()
        return render_template('admin/show_user.html', user_data=user_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

def get_user_data():
    # Retrieve user data from the database (adjust this based on your model)
    user_data = User.query.all()
    return user_data

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/show_pest', methods=['GET', 'POST'])
@login_required
def show_pest():
    try:
        pest_data = get_pest_data()
        return render_template('admin/show_pest.html', pest_data=pest_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

def get_pest_data():
    # Retrieve user data from the database (adjust this based on your model)
    pest_data = Pest.query.all()
    return pest_data

@app.route('/get_pest_details/<int:pest_id>')
def get_pest_details(pest_id):
    pest = Pest.query.get(pest_id)

    if pest:
        pest_data = {
            'pest_name': pest.pest_name,
            'pest_damage': pest.pest_damage,
            'pest_cycle': pest.pest_cycle,
            'pest_control': pest.pest_control,
        }

        # Convert binary data (bytes) to base64 encoding
        if pest.pest_photo:
            pest_data['pest_photo'] = base64.b64encode(pest.pest_photo).decode('utf-8')
        else:
            pest_data['pest_photo'] = None

        return jsonify(pest_data), 200
    else:
        # Return a 404 (NOT FOUND) response if pest is not found
        abort(404)

# @app.route('/add', methods=['GET', 'POST'])
# def add_pest():
#     form = AddPestForm()
#     if form.validate_on_submit():
#         new_pest = Pest(
#             pest_name=form.pest_name.data,
#             pest_damage=form.pest_damage.data,
#             pest_cycle=form.pest_cycle.data,
#             pest_control=form.pest_control.data
#         )
#         db.session.add(new_pest)
#         db.session.commit()
#         flash('Pest added successfully', 'success')
#         return redirect(url_for('show_pest'))
#     return render_template('admin/add_pest.html', form=form)

@app.route('/update_pest/<int:pest_id>', methods=['POST'])
@login_required
def update_pest(pest_id):
    if request.method == 'POST':
        # Handle the form submission, update pest details, etc.
        pest = Pest.query.get(pest_id)
        
        if pest:
            pest_name = request.form.get('pest_name')
            pest_damage = request.form.get('pest_damage')
            pest_cycle = request.form.get('pest_cycle')
            pest_control = request.form.get('pest_control')

            # Update pest details
            pest.pest_name = pest_name
            pest.pest_damage = pest_damage
            pest.pest_cycle = pest_cycle
            pest.pest_control = pest_control

            # Commit changes to the database
            db.session.commit()

            flash('Pest details updated successfully!', 'success')
        else:
            flash('Pest not found!', 'error')

    return redirect(url_for('show_pest'))

@app.route('/delete_pest/<int:pest_id>', methods=['POST'])
def delete_pest(pest_id):
    try:
        pest = Pest.query.get(pest_id)
        if pest:
            db.session.delete(pest)
            db.session.commit()
            return jsonify({'message': 'Pest data deleted successfully'})
        else:
            return jsonify({'error': 'Pest data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/select')
def select():
    csv_path = 'corn.csv'
    df = pd.read_csv(csv_path)
    types = df['type'].unique()
    traits = df['trait'].unique()
    domains = df['domain'].unique()

    log_user_action('Selected something', hist_details='Predicted variety: IES Cn4')

    return render_template('select.html', types=types, traits=traits, domains=domains)

@app.route('/predict', methods=['POST'])
def predict():
    user = current_user

    if request.method == 'POST':
        type_selection = request.form['type']
        trait_selection = request.form['trait']
        domain_selection = request.form['domain']
        planting_date_selection = request.form['target_planting_date']
        target_harvest_date_selection = request.form['target_harvest_date']

        # Assuming df is a CSV loaded DataFrame
        csv_path = 'corn.csv'
        tree_model = C45DecisionTree(csv_path)

        # Predict variety
        predicted_variety, filtered_df, days_to_maturity = tree_model.predict_variety(
            type_selection, trait_selection, domain_selection, planting_date_selection, target_harvest_date_selection
        )

        if predicted_variety:
            planting_date_selection = datetime.strptime(planting_date_selection, '%Y-%m-%d')
            target_harvest_date_selection = datetime.strptime(target_harvest_date_selection, '%Y-%m-%d')

            # Determine season
            season = tree_model.determine_season(planting_date_selection)

            # Query the database to get additional information about the predicted variety
            corn_variety_info = Corn.query.filter_by(variety_name=predicted_variety).first()

            if corn_variety_info:
                # Access information about the corn variety
                variety_name = corn_variety_info.variety_name
                year = corn_variety_info.year
                nsic_regnum = corn_variety_info.nsic_regnum
                variety_type = corn_variety_info.variety_type
                owner = corn_variety_info.owner
                domain = corn_variety_info.domain
                corn_yield = corn_variety_info.corn_yield
                height_dry = corn_variety_info.height_dry
                height_wet = corn_variety_info.height_wet
                ear_length = corn_variety_info.ear_length
                shelling = corn_variety_info.shelling
                lodging = corn_variety_info.lodging
                reaction = corn_variety_info.reaction
                climate = corn_variety_info.climate

                # Retrieve the user's input for farm size
                user_farm_size = float(request.form['farm_size'])  # Assuming it's a numeric field

                # Calculate the possible yield based on farm size
                predicted_yield = corn_variety_info.corn_yield
                possible_yield = predicted_yield * user_farm_size

                log_user_action('Selection', hist_details=f'Type: {type_selection}, Trait: {trait_selection}, Domain: {domain_selection}, Planting Date: {planting_date_selection.date()}, Harvest Date: {target_harvest_date_selection.date()}')


                # Redirect to the result route with the necessary parameters
                return redirect(url_for(
                    'result',
                    user=user,
                    predicted_variety=predicted_variety,
                    type_selection=type_selection,
                    trait_selection=trait_selection,
                    domain_selection=domain_selection,
                    planting_date_selection=planting_date_selection.strftime('%B %d, %Y'),
                    target_harvest_date_selection=target_harvest_date_selection.strftime('%B %d, %Y'),
                    days_to_maturity=days_to_maturity,
                    season=season,
                    predicted_yield=predicted_yield,
                    user_farm_size=user_farm_size,
                    possible_yield=possible_yield,
                    year=year,
                    nsic_regnum=nsic_regnum,
                    variety_type=variety_type,
                    owner=owner,
                    domain=domain,
                    corn_yield=corn_yield,
                    height_dry=height_dry,
                    height_wet=height_wet,
                    ear_length=ear_length,
                    shelling=shelling,
                    lodging=lodging,
                    reaction=reaction,
                    climate=climate,
                    variety_name=variety_name
                ))

    # Handle case where no valid variety is found
    return render_template('result.html', error_message="No valid variety found.")

@app.route('/result')
def result():
    # Retrieve parameters from the query string
    predicted_variety = request.args.get('predicted_variety')
    type_selection = request.args.get('type_selection')
    trait_selection = request.args.get('trait_selection')
    domain_selection = request.args.get('domain_selection')
    planting_date_selection = request.args.get('planting_date_selection')
    target_harvest_date_selection = request.args.get('target_harvest_date_selection')
    days_to_maturity = request.args.get('days_to_maturity')
    season = request.args.get('season')
    predicted_yield = request.args.get('predicted_yield')
    user_farm_size = request.args.get('user_farm_size')
    possible_yield = request.args.get('possible_yield')
    year = request.args.get('year')
    nsic_regnum = request.args.get('nsic_regnum')
    variety_type = request.args.get('variety_type')
    owner = request.args.get('owner')
    domain = request.args.get('domain')
    corn_yield = request.args.get('corn_yield')
    height_dry = request.args.get('height_dry')
    height_wet = request.args.get('height_wet')
    ear_length = request.args.get('ear_length')
    shelling = request.args.get('shelling')
    lodging = request.args.get('lodging')
    reaction = request.args.get('reaction')
    climate = request.args.get('climate')
    variety_name = request.args.get('variety_name')

    log_user_action('Result', hist_details=f'Predicted variety: {predicted_variety}, User Farm Size: {user_farm_size}, Possible yield: {possible_yield}')

    # Render the result template with the retrieved parameters
    return render_template(
        'result.html',
        predicted_variety=predicted_variety,
        type_selection=type_selection,
        trait_selection=trait_selection,
        domain_selection=domain_selection,
        planting_date_selection=planting_date_selection,
        target_harvest_date_selection=target_harvest_date_selection,
        days_to_maturity=days_to_maturity,
        season=season,
        predicted_yield=predicted_yield,
        user_farm_size=user_farm_size,
        possible_yield=possible_yield,
        year=year,
        nsic_regnum=nsic_regnum,
        variety_type=variety_type,
        owner=owner,
        domain=domain,
        corn_yield=corn_yield,
        height_dry=height_dry,
        height_wet=height_wet,
        ear_length=ear_length,
        shelling=shelling,
        lodging=lodging,
        reaction=reaction,
        climate=climate,
        variety_name=variety_name
    )

def log_user_action(action, hist_details=None):
    if current_user.is_authenticated:
        user_history = UserHistory(user_id=current_user.user_id, hist_action=action, hist_details=hist_details)
        db.session.add(user_history)
        db.session.commit()

@app.route('/endpoint', methods=['POST'])
def endpoint():
    # Assuming you have a current_user variable available
    user_id = current_user.user_id  # or current_user.user_id, depending on your model
    # Creating a new UserHistory instance
    user_history = UserHistory(user_id=user_id, hist_action='some_action', hist_timestamp=datetime.now())
    # Adding the instance to the database session
    db.session.add(user_history)
    # Committing the changes to the database
    db.session.commit()

    return redirect(url_for('profile'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_admin()
    app.run(debug=True)