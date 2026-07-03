import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db' # Change to your database name
db = SQLAlchemy(model_class=Base) # Change to your model class
db.init_app(app) # Initialize the database


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Change to your id column
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False) # Change to your name column
    map_url: Mapped[str] = mapped_column(String(500), nullable=False) # Change to your map url column
    img_url: Mapped[str] = mapped_column(String(500), nullable=False) # Change to your image url column
    location: Mapped[str] = mapped_column(String(250), nullable=False) # Change to your location column
    seats: Mapped[str] = mapped_column(String(250), nullable=False) # Change to your seats column
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False) # Change to your has toilet column
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False) # Change to your has wifi column
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False) # Change to your has sockets column
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False) # Change to your can take calls column
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True) # Change to your coffee price column

    def to_dict(self):
        " Convert the cafe object to a dictionary "
        return {column.name: getattr(self, column.name) for column in self.__table__.columns} # Return the cafe as a dictionary

with app.app_context(): # Create the database
    db.create_all() # Create the database


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    " get a random cafe "
    result = db.session.execute(db.select(Cafe)) # select all cafes
    all_cafes = result.scalars().all() # convert to list
    random_cafe = random.choice(all_cafes) # select a random cafe

    return jsonify(cafe=random_cafe.to_dict()) # return the random cafe
@app.route("/all", methods=["GET"])
def get_all_cafes():
    " get all cafes "
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name)) # select all cafes
    all_cafes = result.scalars().all() # convert to list

    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes]) # return all cafes
@app.route("/search", methods=["GET"])
def get_all_cafes_by_location():
    " search cafes at a particular location "
    query_location = request.args.get("loc") # get the location from the query string
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location)) # select all cafes at the location
    all_cafes = result.scalars().all() # convert to list

    if all_cafes: # if there are cafes at the location
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes]) # return all cafes at the location
    else: # if there are no cafes at the location
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404 # return an error

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def create_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    ) # create a new cafe object
    db.session.add(new_cafe) # add the cafe to the database
    db.session.commit() # commit the changes

    return jsonify(response={"success": "Successfully added the new cafe."}) # return a success message

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_coffee_price(cafe_id):
    new_price = request.args.get("new_price") # get the new price from the query string

    try: # try to get the cafe by id
        cafe = db.session.get(Cafe, cafe_id) # get the cafe by id

        if cafe is None: # if the cafe is not found
            raise LookupError("Cafe not found") # raise an error

        cafe.coffee_price = new_price  # update the coffee price
        db.session.commit()  # commit the changes

        return jsonify(response={"success": "Successfully updated the price."}), 200 # return a success message

    except LookupError: # if the cafe is not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404 # return an error

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key") # get the api key from the query string
    if api_key == "TopSecretAPIKey": # if the api key is correct
        try: # try to get the cafe by id
            cafe = db.session.get(Cafe, cafe_id) # get the cafe by id

            if cafe is None: # if the cafe is not found
                raise LookupError("Cafe not found") # raise an error

            db.session.delete(cafe) # delete the cafe
            db.session.commit()  # commit the changes

            return jsonify(response={"success": "Successfully deleted the cafe."}), 200 # return a success message

        except LookupError: # if the cafe is not found
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404 # return an error

    else: # if the api key is not correct
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403 # return an error

if __name__ == '__main__':
    app.run(debug=True)
