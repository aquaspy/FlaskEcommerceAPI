#Importing
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_key_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Product (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# User (id, username, password)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)

#Authentication. This should check which user is trying to use the protected route
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})


@app.route('/api/products/add', methods=["POST"])
@login_required

#Let's use snake case here. 

def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        #data.get allows you to return a default value if the value is blank. data[] does not allows it. It will return an error from the API if the data is empty.
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 200 #No need to add 200 here, but adding it it's ok too
    return jsonify({"message": "Invalid product data"}), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Invalid product ID"}), 404


@app.route('/api/products/<int:product_id>', methods=["GET"])

def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description

        }), 200
    return jsonify({"message": "Product not found."}, 404)

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required

def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found."}, 404)
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
    
    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/api/products', methods=["GET"])

def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = { 
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description

        }
        product_list.append(product_data)
    return jsonify(product_list)


@app.route('/login', methods=["POST"])

def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "Logged in successfully"})

    return jsonify({"message": "Unauthorized. Invalid crendentials"})
    


#Main page (/)
@app.route('/')
def hello_world():
    return 'Hello world!'

#Just for developing, disable debug mode on production. This check is to make sure that the file is executed directly.
if __name__ == "__main__":
    app.run(debug=True)