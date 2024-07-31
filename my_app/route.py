from flask import render_template, url_for, redirect, flash, request
from my_app import app, db, bcrypt, mail
from my_app.forms import RegistrationForm, LoginForm, RequestRsetForm, ResetPasswordForm
import requests
from my_app.models import User
from flask_login import login_user, current_user, logout_user
from flask_mail import Message
def custom_round(number):
    # Check if the number is positive, negative, or zero
    if number > 0:
        # Round to 2 decimal places for positive numbers
        return round(number, 2)
    elif number < 0:
        # Round to 4 decimal places for negative numbers
        return round(number, 4)
    else:
        # Special handling for zero
        # Assuming you want to keep the leading zeros for negative numbers
        if number == 0:
            return 0
        else:
            # For negative zeros, round to 4 decimal places
            return round(number, 4)
apikey = 'b6a8f90f-c980-429a-bdf9-54f3a1b7662a'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey
}
parames = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
listing_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

 # getting the coin and setting the start and limit
def get_coins(start, limit):
    parames['start'] = start
    parames['limit'] = limit
    response = requests.get(listing_url, params=parames, headers=headers).json()
    return response['data']

@app.route("/home")
@app.route("/")
def homepage():
   
    page = request.args.get('page', 1 , type=int)
    limit = 100
    start = (page - 1) * limit + 1

     # Get all coins to calculate the total number of pages
    all_coins = get_coins(1, 5000)
    total_coins = len(all_coins)
    total_pages = (total_coins // limit) + (1 if total_coins % limit != 0 else 0)

    # 
   
    coin_listings = get_coins(start, limit)
    sn = start
    #coin_listings = json['data']
    #sn = 1
    if current_user.is_authenticated:
        image = url_for('static', filename='Images/' + current_user.image)
        for coin in coin_listings:
            coin['quote']['USD']['price'] = custom_round(coin['quote']['USD']['price'])
            coin['sn'] = sn
            sn += 1
        return render_template('home.html',coins=coin_listings, image=image, page=page,total_pages=total_pages, limit=10)
        
        # Iterate over each coin and increment the counter
    for coin in coin_listings:
        coin['quote']['USD']['price'] = custom_round(coin['quote']['USD']['price'])
        coin['sn'] = sn
        sn += 1
    
    return render_template('home.html', coins=coin_listings,page=page,total_pages=total_pages, limit=10)
    #else:
        #return "Failed to fetch data."


@app.route("/Account")
def Account():
    image = url_for('static', filename='Images/' + current_user.image)
    return render_template('Account.html', image = image)


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('Register.html', title = "title", form = form)


@app.route("/login", methods = ['GET','POST']) 
def login():

    """"here handle login page"""
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('homepage'))
    return render_template('login.html', title = "title", form = form)

@app.route("/logout") 
def logout():
    logout_user()
    return redirect(url_for('homepage'))

def send_email(user):
    token = user.get_reset_token()
    mess = Message('password request reset', sender='mclaret797@gmail.com', recipients=[user.email])

    mess.body= f'''
To reset your password click the link below:
{url_for('Request_token', token=token, _external=True)}
'''
    mail.send(mess)


@app.route("/Reset_Password", methods=['GET','POST'])
def Request_Reset():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RequestRsetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Email has been sent to you', 'infor')
        return redirect(url_for('login'))
    return render_template('Request_token.html', title = "Reset password", form = form)

@app.route("/Reset_Password/<token>", methods=['GET','POST'])
def Request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    user = User.get_verify_token(token)
    if user is None:
        flash('the token is invalid or expired', 'Warning')
        return redirect(url_for('Request_token'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hash_password
            db.session.commit()
            flash('succesful updated')
            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f"Error updating password: {e}")
            flash('An error occurred while resetting your password. Please try again.', 'danger')
    return render_template('Reset_token.html', form=form)
