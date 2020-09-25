from flask import render_template, url_for,flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post

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
   form= LoginForm()
   if form.validate_on_submit():
      if form.email.data == 'admin@log.com' and form.password.data == 'password':
         flash('You have been logged in!', 'success')
         return redirect(url_for('homepage'))
      else:
         flash('Login Unsuccesful.','danger')
   return render_template('login.html', title = 'Login', form = form)


 # about
@app.route("/about")
def about():
   return render_template('home.html', title = 'About')

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
