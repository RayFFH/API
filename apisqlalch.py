from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


# noinspection PyUnresolvedReferences
class Product(db.Model):
    first_name = db.Column(db.String(100), unique= True)
    last_name = db.Column(db.String(100), unique=True)
    id = db.Column(db.Integer)

    def __init__(self, first_name,last_name,grade):
        self.first_name= first_name
        self.last_name = last_name
        self.grade = grade


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('grade','first_name','last_name')


product_schema = ProductSchema(strict = True)
products_schema = ProductSchema(many=True, strict=True)


@app.route('/product', methods=['POST'])
def add_product():
    first_name=request.json['first_name']
    last_name = request.json['last_name']
    grade = request.json['last_name']

    new_product = Product(first_name, last_name, grade)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonyif(new_product)


if __name__ == '__main__':
    app.run(debug= True)
