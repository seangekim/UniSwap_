import pymongo
from pymongo import MongoClient


from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import Users


app = Flask(__name__)

cluster = MongoClient("mongodb+srv://cjdewitt:d8ZpfzggeDVYvHMO@uni-swap.hy9bzs8.mongodb.net/?retryWrites=true&w=majority")
db = cluster["uni-swap"]
collection = db["Products"]


# Set up file upload directory and allowed file extensions
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Define the home page route
@app.route("/")
def home():
    # Get all products from the database
    products = collection.find()
    return render_template("home.html", products=products)

# Define the product page route
@app.route("/product/<product_id>")
def product(product_id):
    # Get the product with the specified ID from the database
    product = collection.find_one({"_id": product_id})
    return render_template("product.html", product=product)

# Define the post product route
@app.route("/post_product", methods=["GET", "POST"])
def post_product():

    user = Users()

    # Check if the user is logged in
    if user.is_logged_in() == False:
        return redirect(url_for('login'))

    else:
        if request.method == "POST":
            # Get the product information from the form
            name = request.form["name"]
            price = request.form["price"]
            image_file = request.files["image"]
            description = request.form["description"]

            # Validate the form data
            if not name:
                return "Name is required"
            if not price:
                return "Price is required"
            if not image_file or not allowed_file(image_file.filename):
                return "Please upload a valid image file"

            # Save the image file to disk
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            if collection.find({"name": name}, {"price": price}, {"image": filename}, {"description": description}):
                # Insert the product into the database
                product = {
                    "name": name,
                    "price": price,
                    "image": filename,
                    "description": description
                }
                collection.insert_one(product)

            # Redirect to the home page
            return redirect(url_for("home"))

        else:
            # Render the product form
            return render_template("post_product.html")



if __name__ == "__main__":
    app.run(debug=True)
