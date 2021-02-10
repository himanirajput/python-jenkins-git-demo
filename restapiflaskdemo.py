# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:51:10 2021

@author: HimaniRajput

In express : app = express()
             app.get('',())
             app.post('',())
             
             
SQLAlchemy : ORM - object-relation mapping             
"""

import json
from flask import Flask,jsonify,request,Response,make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)                  #configuring flask to connect to db
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:admin@localhost:3306/devops'

db=SQLAlchemy(app)

#creating table using python 
class Product(db.Model):               #table is a model
    __tablename__="pyproducts"
    productId=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(40))
    description=db.Column(db.String(60))
    productCode=db.Column(db.String(40))
    price=db.Column(db.Float)
    starRating=db.Column(db.Float)
    imageUrl=db.Column(db.String(40))

    def create(self):                #this method is getting overridden
        db.session.add(self)         #gets connection to db
        db.session.commit()
        return self
        
    def __init__(self,productName,description,productCode,price,starRating,imageUrl):
        self.productName = productName
        self.description = description
        self.productCode = productCode
        self.price = price
        self.starRating = starRating
        self.imageUrl = imageUrl
        
    def __repr__(self):                        #representation - official string representation of object
        return "%self.productId"
    
db.create_all()



#map objects to tables: object-relation mapping
class ProductSchema(ModelSchema):  #ProductSchema extends ModelSchema i.e ProductSchema is a ModelSchema
    class Meta(ModelSchema.Meta):     #nested classes : inner class
        model = Product
        sqla_session = db.session
    
    #moving back to outer class
    productId = fields.Number(dump_only=True)    
    productName = fields.String(required=True)       # required means indicating that the field is mandatory
    description = fields.String(required=True)
    productCode = fields.String(required=True)
    price = fields.Number(required=True)
    starRating = fields.Number(required=True)
    imageUrl = fields.String(required=True)

#decorators
@app.route('/products',methods=['POST'])
def createProduct():
    data = request.get_json()      #as it a json data, get json data sent by client
    product_schema = ProductSchema()
    product = product_schema.load(data)   # unmarshalling - mapping the data back to objects
    result = product_schema.dump(product.create())   #inserting into db ; it is using flask module ; if flask wasn't used , we would have to write queries manually
    return make_response(jsonify({"product":result}),201)      # 201 - success , _____ is created

@app.route('/products',methods=['GET'])
def getAllProducts():
    get_products=Product.query.all()
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({"products":products}),200)


@app.route('/products/<int:productId>',methods=['GET'])
def getProductById(productId):
    get_product=Product.query.get(productId)
    productSchema=ProductSchema()
    product=productSchema.dump(get_product)
    return make_response(jsonify({"product":product}),200)


@app.route('/products/<int:productId>',methods=['DELETE'])      #Dependency Injection <int:productId>
def deleteProductById(productId):
    get_product=Product.query.get(productId)
    
    db.session.delete(get_product)
   
    db.session.commit()                         # since it is a crud operation
    return make_response(jsonify({"result":"product deleted"}),204)


@app.route('/products/<int:productId>',methods=['PUT'])
def updateProduct(productId):
    data = request.get_json()      #as it a json data, get json data sent by client
    get_product=Product.query.get(productId)
    if data.get('price'):
        get_product.price = data['price']
    
    db.session.add(get_product)
    db.session.commit()    
    product_schema = ProductSchema(only = ['productId','price'])
    result = product_schema.dump(get_product)  
    return make_response(jsonify({"product":result}),200)


@app.route('/products/find/<productName>',methods=['GET'])
def getProductByName(productName):
    get_products=Product.query.filter_by(productName=productName)      #its like - select * from products where name=(productName)
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({"product":products}),200)

app.run(port=4002)    


    
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
   
    
    
    
    
    
    
    
    
    
    