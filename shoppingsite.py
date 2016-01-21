"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, session, render_template, redirect, flash
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'SEEKRIT'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types


    total_order_cost = 0

    # list of tuples of name, qty, price, total
    individual_melon_order = []
    
    for melon_id in session['cart']:
        melon_quantity = session['cart'].count(melon_id)
        melon_name = melons.get_by_id(melon_id).common_name
        melon_price = melons.get_by_id(melon_id).price
        melon_total = melon_quantity * melon_price
        melon_tuple = (melon_name, melon_quantity, melon_price, melon_total)
        total_order_cost += melon_total     
        if melon_tuple not in individual_melon_order:
            individual_melon_order.append(melon_tuple)

        # melon_name, melon_quantity, melon_price, melon_total = melon_tuple

    # print individual_melon_order
    for melon_tuple in individual_melon_order:
        melon_name, melon_quantity, melon_price, melon_total = melon_tuple



    return render_template("cart.html", 
                            melon_order=individual_melon_order,
                            name=melon_name,
                            quantity=melon_quantity,
                            price=melon_price,
                            total=melon_total,
                            order_total=total_order_cost)
    # return render_template("cart.html", 
    #                         melon_order=individual_melon_order,
    #                         order_total=total_order_cost)



@app.route("/add_to_cart/<int:melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session


    # session = {'cart': [17, 15, 17]}

    # import pdb; pdb.set_trace()


    cart = session.get('cart', [])
    cart.append(melon_id)
    flash("Melon successfully added to cart!")
    session['cart'] = cart
    print session['cart']

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
