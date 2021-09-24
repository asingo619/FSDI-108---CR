from mock_data import mock_data
import json
from flask import Flask, render_template, abort, request
app = Flask(__name__)

# put the dict here.
me = {
    "name" :"Andrew",
    "last" : "Singo",
    "email" : "test@email.com",
    "age" : 32,
    "hobbies" : [],
    "address" : {
        "street" : "main st",
        "number" : "100"
    }

}

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    # return full name.
    return f"{me['name']} {me['last']}"

@app.route("/about/email")
def email_info():
    return f"{me['email']}"

@app.route("/about/address")
def address_info():
    address = me ['address']
    return f"{address['number']} {address['street']}"


#### API Methods

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    print(request.headers)
    return json.dumps(mock_data)

@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    
    if not "price" in product or product["price"] <= 0:
        abort(400, "Price required and must be greater than zero")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and should be at least 5 chars long")

    mock_data.append(product)
    product["_id"] = len(product["title"])
    return json.dumps(product)   


@app.route("/api/categories")
def get_categories():
    
    categories = []
    for product in mock_data:
        cat = product["category"]

        if cat not in categories:
            categories.append(cat)
    
    return json.dumps(categories)

@app.route("/api/product/<id>")
def get_by_id(id):
    # find the porduct with such id
    # return the product as json string
    found = False
    for prod in mock_data:
        if prod["_id"] == id:
            found = True
            return json.dumps(prod)

    if not found:       
        abort(404)


@app.route("/api/catalog/<cat>")
def get_by_category(cat):
    prods = []
    for prod in mock_data:
        if prod["category"].lower() == cat.lower():
            prods.append(prod)
        
    return json.dumps(prod)

@app.route("/api/cheapest") 
def get_cheapest():
    cheapest = mock_data[0]
    for prod in mock_data:
        if prod ["price"] < cheapest["price"]:
            cheapest = prod

    return json.dumps(cheapest)   


app.run(debug = True)
