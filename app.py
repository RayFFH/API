from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(100), unique=True)
  lastname = db.Column(db.String(100))
  grade = db.Column(db.String(100))
  

  def __init__(self, firstname, lastname, grade):
    self.firstname = firstname
    self.lastname = lastname
    self.grade = grade
    

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'firstname', 'lastname', 'grade')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# homepage
@app.route("/")
def homepage():
      return render_template('homepage.html')

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
   firstname = request.json['firstname']
   lastname = request.json['lastname']
   grade = request.json['grade']
   
   new_product = Product(firstname, lastname, grade)

   db.session.add(new_product)
   db.session.commit()

   return product_schema.jsonify(new_product)


# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
   all_products = Product.query.all()
   result = products_schema.dump(all_products)
   return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
   product = Product.query.get(id)
   return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
   product = Product.query.get(id)

   firstname = request.json['firstname']
   lastname = request.json['lastname']
   grade = request.json['grade']

   product.firstname = firstname
   product.lastname = lastname
   product.grade = grade

   db.session.commit()

   return product_schema.jsonify(product)

#Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
   product = Product.query.get(id)
   db.session.delete(product)
   db.session.commit()

   return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)