"""
Write a script that starts a Flask web application:

    Your web application must be listening on 0.0.0.0, port 5000
    You must use storage for fetching data from the storage engine
    (FileStorage or DBStorage) => from models import storage and
    storage.all(...)
    To load all cities of a State:
        If your storage engine is DBStorage, you must use cities relationship
        Otherwise, use the public getter method cities
    After each request you must remove the current SQLAlchemy Session:
        Declare a method to handle @app.teardown_appcontext
        Call in this method storage.close()
    Routes:
        /hbnb: display a HTML page like 8-index.html, done during the 0x01.
        AirBnB clone - Web static project
            Copy files 3-footer.css, 3-header.css, 4-common.css, 6-filters.css
            and 8-places.css from web_static/styles/ to the folder
            web_flask/static/styles
            Copy all files from web_static/images/ to the folder
            web_flask/static/images
            Update .popover class in 6-filters.css to enable scrolling in the
            popover and set max height to 300 pixels.
            Update 8-places.css to always have the price by night on the top
            right of each place element, and the name correctly aligned and
            visible (i.e. screenshots below)
        Use 8-index.html content as source code for the template
        100-hbnb.html:
            Replace the content of the H4 tag under each filter title
            (H3 States and H3 Amenities) by &nbsp;
            Make sure all HTML tags from objects are correctly used
            (example: <BR /> must generate a new line)
            State, City, Amenity and Place objects must be loaded from
            DBStorage and sorted by name (A->Z)
    You must use the option strict_slashes=False in your route definition
"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """hbnb"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    print(list(amenities.values())[0].name)

    return render_template(
        "100-hbnb.html",
        states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def app_teardown(args=None):
    """teardown app"""
    if args:
        pass
    storage.close()


if __name__ == "__main__":
    app.run(debug=1, host="0.0.0.0", port=5000)
