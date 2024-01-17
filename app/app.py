from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from bson import ObjectId
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure SQL database for user table
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://db_user:db_password@sql_db/product_catalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure NoSQL database for product table
app.config['MONGO_URI'] = 'mongodb://nosql_db:27017/product_catalog'
mongo = PyMongo(app)

# Configure JWT
# Change this to a secure random key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app, False)


bcrypt = Bcrypt(app)

# Define SQL User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_number = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


# Define MongoDB product collection
product_collection = mongo.db.products

# Request body schema for user registration
registration_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "contact_number": {"type": ["string", "null"]},
        "password": {"type": "string"},
        "confirm_password": {"type": "string"},
    },
    "required": ["username", "email", "password", "confirm_password"],
    "additionalProperties": False
}

# Request body schema for user login
login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
    "additionalProperties": False
}

# Request body schema for product addition
product_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": "number"},
        "category": {"type": "string"},
        "stock_quantity": {"type": "integer"},
    },
    "required": ["name", "description", "price", "category", "stock_quantity"],
    "additionalProperties": False
}

# API endpoints
# User registration endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        validate(instance=data, schema=registration_schema)
    except ValidationError as e:
        return jsonify(message="Invalid request body", error=str(e)), 400
    
    if data['password'] == data['confirm_password']:
        new_user = User(
            username=data['username'],
            email=data['email'],
            contact_number=data.get('contact_number', None)
        )
        new_user.set_password(data['password'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message='User registered successfully'), 201
        except IntegrityError as error:
            db.session.rollback()
            return jsonify(message='Username already exists', error=str(error)), 409
        except Exception as error:
            return jsonify(message=f'Exception Occurred', error=str(error)), 500
    else:
        return jsonify(message="User registration failed, password didn't match"), 500



# User login endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    try:
        validate(instance=data, schema=login_schema)
    except ValidationError as e:
        return jsonify(message="Invalid request body", error=str(e)), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid username or password'), 401


# Protected endpoint - Requires JWT token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Product listing endpoint


@app.route('/products', methods=['GET'])
def list_products():
    products = product_collection.find({}, {'_id': False})
    return jsonify(products=list(products))


# Product addition endpoint - Requires JWT token
@app.route('/add_product', methods=['POST'])
@jwt_required()
def add_product():
    product = request.json

    try:
        validate(instance=product, schema=product_schema)
    except ValidationError as e:
        return jsonify(message="Invalid request body", error=str(e)), 400
    
    product['created_at'] = datetime.utcnow()
    product['updated_at'] = datetime.utcnow()
    existing_product = mongo.db.products.find_one({"name": product['name']})
    if existing_product:
        # If the product exists, update its fields
        result = mongo.db.products.update_one(
            {"name": product['name']},
            {"$set": {
                "description": product['description'],
                "price": product['price'],
                "stock_quantity": product['stock_quantity'],
                "category": product['category'],
                "updated_at": product['updated_at']
            }}
        )

        if result.modified_count > 0:
            return jsonify(message=f'Product "{product[f"name"]}" updated successfully'), 200
        else:
            return jsonify(message='Failed to update product'), 500
    else:
        # If the product does not exist, insert a new product
        result = mongo.db.products.insert_one(product)

        if result.inserted_id:
            return jsonify(message='Product added successfully', product_id=str(result.inserted_id)), 201
        else:
            return jsonify(message='Failed to add product'), 500


# Product details retrieval endpoint - Requires JWT token
@app.route('/product/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    try:
        current_user = get_jwt_identity()
        product = product_collection.find_one({'_id': ObjectId(product_id)}, {'_id': False})
        if product:
            return jsonify(product=product), 200
        else:
            return jsonify(message='Product not found'), 404
    except Exception as e:
        return jsonify(message=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
