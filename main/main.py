from producer import publish
import json
import requests
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app=app)

@dataclass
class Product(db.Model):
    id:int
    title:str
    image:str

    # product will be created from Django app, not Flask, so autoincrement to False
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # to make sure every composite key (combination) of user_id and product_id is unique
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')



@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    request = requests.get('http://docker.for.mac.localhost:8000/api/user') # docker host
    request_json = request.json()
    try:
        productUser = ProductUser(user_id=request_json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except Exception as exp:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')