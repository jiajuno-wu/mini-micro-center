from flask import Blueprint, render_template, redirect,url_for,flash
from ltt.forms import Additem , CommentForm, RateForm, RegisterUser,LoginForm
from ltt import app
from ltt import db
from ltt.models import Item, Comment, User
from flask_login import login_user, current_user

import random

view = Blueprint("view",__name__)

TABOO = ["dead","death"]

@view.route('/')
@view.route('/home')   #home page to show all the item
def home():
    items = Item.query.all()
    return render_template("home.html", items = items)



@view.route('/additem',methods = ['GET','POST'])  #page for staff to add item
def additem():
    form = Additem()
   
    if form.validate_on_submit():  # function is called when press submit button
        item_to_add = Item(
                       item_name = form.item_name.data,
                       item_price = form.item_price.data,
                       item_image = form.item_image.data,
                       item_type = form.item_type.data,
                       item_c = form.item_c.data,)
        db.session.add(item_to_add)
        db.session.commit()
        return redirect(url_for('view.additem'))
    return render_template('additems.html',form=form)



@view.route('/displayItem')   #page for staff to view item
def displayItem():
    items = Item.query.all()
    return render_template('displayItem.html', items = items)




@view.route('/delete/<int:id>')  #a route bind to a delete button hit when the button is pressed
def delete(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('view.displayItem'))
    except:
        return 'There was an error deleting'




@view.route('/itempage/<int:items_id>', methods = ['GET','POST'])   #item page
def views(items_id):
    item_to_show = Item.query.get_or_404(items_id)
    c = Comment.query.filter_by(item_id = items_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        # if form.content.data contain taboo then give  warning
        text = form.content.data
        text = text.split(' ')
        for t in TABOO:
            if t in text : 
                current_user.warnings = current_user.warnings + 1
                db.session.commit()
                if current_user.warnings == 3:
                    current_user.status = "Invalid"
                    db.session.commit()
                
                flash('Your comment contain taboo',category = 'danger')
                return redirect(url_for('view.views', items_id = items_id)) 
        
        comment = Comment(content = form.content.data, item_id = items_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view.views', items_id = items_id))

    rform = RateForm()
    if rform.validate_on_submit():
        item_to_show.rate_count = item_to_show.rate_count + 1
        item_to_show.rate_acc = item_to_show.rate_acc + rform.rate.data
        db.session.commit()
        return redirect(url_for('view.views', items_id = items_id))
    
    return render_template('item.html',item_to_show = item_to_show,c = c ,form = form, rform = rform)


@view.route('/register',methods = ['GET','POST']) #Register route for users
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        user_to_add = User(username=form.username_.data, 
                            password=form.password_.data
                            )
        db.session.add(user_to_add)
        db.session.commit()
        return redirect(url_for('view.register'))
    return render_template('register.html', form = form)

@view.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username_.data).first()
        if attempted_user and attempted_user.check_password_correction (attempted_password = form.password_.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as :{attempted_user.username}', category = 'success')
            return render_template('success.html')
        else:
            flash('Username and password is incorrect! Please try again',category = 'danger')
            return render_template('failure.html')

    return render_template('login.html',form=form)