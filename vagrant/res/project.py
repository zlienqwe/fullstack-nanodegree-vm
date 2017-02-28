from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')

@app.route('/restaurants')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menuitems.html', restaurant = restaurant, items = items)


# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(name = request.form['NewItem'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("create a new item")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newItem.html', restaurant = restaurant)


# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        editItem = session.query(MenuItem).filter_by(id=menu_id).one()
        editItem.name = request.form['editedMenuItem']
        session.add(editItem)
        session.commit()
        flash("changes item's name")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editItem.html', restaurant = restaurant, menuItem = menuItem)


# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(deleteItem)
        session.commit()
        flash("delete a item")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('deleteItem.html', restaurant = restaurant, item = item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)