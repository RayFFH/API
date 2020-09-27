from flask import render_template, url_for,flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Post
from flask_login import login_user, current_user,logout_user, login_required
import secrets, os
posts = [
   {
      'author': 'Maria Smith',
      'title': 'The shining',
      'content': 'First post',
      'date_posted': 'Sept 20, 2020'
   },
   {
      'author': 'Maria Smith',
      'title': 'The shining 2',
      'content': 'secibd post',
      'date_posted': 'Sept 21, 2020'
   }
]

# # Product Class/Model
# class Product(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   firstname = db.Column(db.String(100), unique=True)
#   lastname = db.Column(db.String(100))
#   grade = db.Column(db.String(100))
  

#   def __init__(self, firstname, lastname, grade):
#     self.firstname = firstname
#     self.lastname = lastname
#     self.grade = grade
    

# # Product Schemastop
# class ProductSchema(ma.Schema):
#   class Meta:
#     fields = ('id', 'firstname', 'lastname', 'grade')

# # Init schema
# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)

# homepage
@app.route("/")
def homepage():
   return render_template('home.html', posts = posts)

# Register
@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now log in','success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

# Login
@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login Unsuccesful.','danger')
    return render_template('login.html', title = 'Login', form = form)


 # about
@app.route("/about")
def about():
   return render_template('home.html', title = 'About')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form =  UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title = 'Account',
                        image_file=image_file, form=form)

# # Create a Product
# @app.route('/product', methods=['POST'])
# def add_product():
#    firstname = request.json['firstname']
#    lastname = request.json['lastname']
#    grade = request.json['grade']
   
#    new_product = Product(firstname, lastname, grade)

#    db.session.add(new_product)
#    db.session.commit()

#    return product_schema.jsonify(new_product)


# # Get All Products
# @app.route('/product', methods=['GET'])
# def get_products():
#    all_products = Product.query.all()
#    result = products_schema.dump(all_products)
#    return jsonify(result)

# # Get Single Products
# @app.route('/product/<id>', methods=['GET'])
# def get_product(id):
#    product = Product.query.get(id)
#    return product_schema.jsonify(product)

# # Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#    product = Product.query.get(id)

#    firstname = request.json['firstname']
#    lastname = request.json['lastname']
#    grade = request.json['grade']

#    product.firstname = firstname
#    product.lastname = lastname
#    product.grade = grade

#    db.session.commit()

#    return product_schema.jsonify(product)

# #Delete Product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#    product = Product.query.get(id)
#    db.session.delete(product)
#    db.session.commit()

#    return product_schema.jsonify(product)
